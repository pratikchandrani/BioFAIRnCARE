"""PV rules: participant identifiers and credentials must never be stored (research R11)."""

from __future__ import annotations

import re

from ..vault import MEMBERS_NOTE
from . import finding

ALLOW_RE = re.compile(r"%%\s*pv-allow:[^%]*%%")
PREFILTER = re.compile(r"\d|@|[A-Z]{5}|(?i:patient\s*name|mrn|uhid|dob|date\s*of\s*birth|hospital)")
CREDENTIAL_HINTS = ("ghp_", "gho_", "ghu_", "ghs_", "ghr_", "github_pat_", "glpat-", "private key", "password")
IDENTIFIER_PATTERNS = [
    ("Indian mobile number", re.compile(r"(?<![\w-])(?:\+91[-\s]?)?[6-9]\d{9}(?![\w-])")),
    ("Aadhaar-like 12-digit number", re.compile(r"(?<![\w-])\d{4}\s\d{4}\s\d{4}(?![\w-])|(?<![\w-])\d{12}(?![\w-])")),
    ("PAN-like identifier", re.compile(r"(?<![\w-])[A-Z]{5}\d{4}[A-Z](?![\w-])")),
    ("labelled patient identifier", re.compile(
        r"\b(MRN|UHID|hospital\s*(?:no|number|id)|patient\s*name|DOB|date\s*of\s*birth)\b\s*[:=#-]\s*[\w/.-]+",
        re.I)),
    ("e-mail address", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
]
CREDENTIAL_PATTERNS = [
    ("GitHub token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("password value", re.compile(r"\bpassword\s*[:=]\s*\S{4,}", re.I)),
]


def _lines_without_allowed(text: str):
    for i, line in enumerate(text.split("\n"), start=1):
        if ALLOW_RE.search(line):
            continue
        yield i, line


def pv001(ctx):
    for note in ctx.vault.notes:
        if note.rel == MEMBERS_NOTE:
            continue
        severity = "error" if note.data.get("human_or_community_data") is True else "warning"
        text = note.text
        for lineno, line in _lines_without_allowed(text):
            if not PREFILTER.search(line):
                continue
            for label, pat in IDENTIFIER_PATTERNS:
                if label == "e-mail address" and "@" not in line:
                    continue
                m = pat.search(line)
                if m:
                    if label == "e-mail address" and note.rel.startswith("Resources/lab_resources/"):
                        continue
                    yield finding("PV001", severity, note, f"possible {label}: {m.group(0)[:4]}…", lineno,
                                  "remove it; use de-identified codes only (or add %% pv-allow: reason %% "
                                  "on the line after review)")


def pv002(ctx):
    files = [(n.rel, n.text) for n in ctx.vault.notes] + [(t.rel, t.text) for t in ctx.vault.templates]
    obs = ctx.vault.root / ".obsidian"
    if obs.is_dir():
        for path in obs.rglob("*.json"):
            rel = path.relative_to(ctx.vault.root).as_posix()
            if rel.endswith("obsidian-git/data.json"):
                continue
            files.append((rel, path.read_text(encoding="utf-8", errors="replace")))
    for rel, text in files:
        low = text.lower()
        if not any(h in low for h in CREDENTIAL_HINTS):
            continue
        for lineno, line in _lines_without_allowed(text):
            for label, pat in CREDENTIAL_PATTERNS:
                if pat.search(line):
                    yield finding("PV002", "error", rel, f"possible {label} in a versioned file", lineno,
                                  "remove it and rotate the credential")


RULES = {"PV001": pv001, "PV002": pv002}
