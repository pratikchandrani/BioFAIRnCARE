"""SO rules: reviewer-committed sign-off and append-only records after sign-off (FR-007a/b)."""

from __future__ import annotations

import re

from ..gitcheck import before_heading, normalise_body, split_note
from ..vault import scrub
from . import conditional_findings, finding

AMENDMENTS = "## Amendments"
AMEND_RE = re.compile(r"^- \d{4}-\d{2}-\d{2} (—|--) .+? (—|--) .+")
VOLATILE = {"updated"}


def _signed_off(ctx):
    for note in ctx.typed_notes():
        if note.type == "experiment" and note.data.get("status") in ("signed-off", "archived") \
                and note.data.get("signed_off_by"):
            yield note


def _signoff_version(ctx, note):
    for version in ctx.git.versions(note.rel):
        data, _ = split_note(version.content)
        if data.get("status") == "signed-off":
            return version
    return None


def so000(ctx):
    if ctx.git is not None and ctx.git.available:
        return
    for note in _signed_off(ctx):
        yield finding("SO000", "unverifiable", note, "no Git history available; sign-off cannot be verified")


def so001(ctx):
    yield from conditional_findings(ctx, "SO001")


def so002(ctx):
    if ctx.git is None or not ctx.git.available:
        return
    for note in _signed_off(ctx):
        name = note.data.get("signed_off_by")
        reviewer = ctx.vault.reviewer_by_name(name)
        if reviewer is None:
            yield finding("SO002", "error", note, f"'{name}' is not an active reviewer in Lab members",
                          note.line_of("signed_off_by"))
            continue
        version = _signoff_version(ctx, note)
        if version is None:
            yield finding("SO002", "error", note, "sign-off is not committed yet; the reviewer must commit it",
                          note.line_of("status"))
        elif version.email != reviewer.git_email:
            yield finding("SO002", "error", note,
                          f"sign-off committed by {version.email} ({version.sha[:7]}), not by reviewer "
                          f"{reviewer.name} <{reviewer.git_email}>", note.line_of("signed_off_by"),
                          "the reviewer must re-commit the sign-off under their own Git identity")


def so003(ctx):
    if ctx.git is None or not ctx.git.available:
        return
    for note in _signed_off(ctx):
        version = _signoff_version(ctx, note)
        if version is None:
            continue
        old_fm, old_body = split_note(version.content)
        new_fm, new_body = split_note(note.text)
        ignore = set(VOLATILE)
        if new_fm.get("status") == "archived":
            ignore.add("status")
        changed = sorted(k for k in set(old_fm) | set(new_fm)
                         if k not in ignore and old_fm.get(k) != new_fm.get(k))
        if changed:
            yield finding("SO003", "error", note, "properties changed after sign-off: " + ", ".join(changed),
                          suggestion="revert and record the correction under '## Amendments'")
        old_main, _ = before_heading(old_body, AMENDMENTS)
        new_main, _ = before_heading(new_body, AMENDMENTS)
        if normalise_body(old_main) != normalise_body(new_main):
            yield finding("SO003", "error", note,
                          f"content above '{AMENDMENTS}' changed after sign-off ({version.sha[:7]})",
                          suggestion="restore the signed-off text; add corrections as dated amendments")


def so004(ctx):
    for note in ctx.typed_notes():
        if note.type != "experiment":
            continue
        body_lines = scrub(note.fm.body.replace("\r\n", "\n")).split("\n")
        try:
            idx = next(i for i, ln in enumerate(body_lines) if ln.strip() == AMENDMENTS)
        except StopIteration:
            continue
        for i in range(idx + 1, len(body_lines)):
            s = body_lines[i].strip()
            if s.startswith("## "):
                break
            if s.startswith("- ") and not AMEND_RE.match(s):
                yield finding("SO004", "warning", note, "amendment must read '- YYYY-MM-DD — Name — text'",
                              note.fm.body_start_line + i)


RULES = {"SO000": so000, "SO001": so001, "SO002": so002, "SO003": so003, "SO004": so004}
