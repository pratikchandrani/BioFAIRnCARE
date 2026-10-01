"""Vault model: notes, attachments, links, lab members, settings, plugin register."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

from . import frontmatter as fmlib
from .schema import Schema

SKIP_DIRS = {".git", ".obsidian", ".trash", "__pycache__"}
TEMPLATES_DIR = "Resources/templates/"            # Templater picker: daily + commands
NOTE_TEMPLATES_DIR = "Resources/note-templates/"  # experiment / record templates and local copies
TEMPLATE_DIRS = (TEMPLATES_DIR, NOTE_TEMPLATES_DIR)
TOOLS_DIR = "Resources/tools/"
LAB_RESOURCES_DIR = "Resources/lab_resources/"
EXAMPLES_DIR = "_Examples/"
SETTINGS_NOTE = "Resources/Vault settings.md"
MEMBERS_NOTE = "Resources/lab_resources/Lab members.md"
PLUGIN_REGISTER = "Resources/lab_resources/Plugin register.md"
NON_ATTACHMENT_NAMES = {".gitkeep", ".gitignore", "LICENSE", "VERSION", "lab-owned.txt"}
NON_ATTACHMENT_EXT = {"md", "base", "canvas"}

FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
COMMENT_RE = re.compile(r"%%.*?%%", re.S)
TEMPLATER_RE = re.compile(r"<%.*?%>", re.S)
WIKI_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
MD_LINK_RE = re.compile(r"(!?)\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


@dataclass
class Finding:
    rule: str
    severity: str  # error | warning | info | unverifiable
    path: str
    message: str
    line: int | None = None
    suggestion: str | None = None

    def as_dict(self) -> dict:
        return {"rule": self.rule, "severity": self.severity, "path": self.path,
                "line": self.line, "message": self.message, "suggestion": self.suggestion}


@dataclass
class Link:
    target: str
    line: int
    embed: bool
    source: str  # "body" | property name


@dataclass
class Note:
    rel: str
    path: Path
    text: str
    fm: fmlib.Frontmatter | None = None
    fm_error: fmlib.FrontmatterError | None = None
    links: list = field(default_factory=list)

    @property
    def data(self) -> dict:
        return self.fm.data if self.fm else {}

    @property
    def type(self):
        return self.data.get("type")

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def is_example(self) -> bool:
        return self.rel.startswith(EXAMPLES_DIR)

    def line_of(self, key: str) -> int | None:
        return self.fm.lines.get(key) if self.fm else None


@dataclass
class Member:
    name: str
    initials: str
    role: str
    git_email: str
    status: str

    @property
    def is_reviewer(self) -> bool:
        return self.status == "active" and self.role in ("reviewer", "pi")


class Vault:
    def __init__(self, root: Path, schema: Schema):
        self.root = root
        self.schema = schema
        self.notes: list[Note] = []
        self.templates: list[Note] = []
        self.attachments: list[str] = []
        self.other_files: list[str] = []
        self._scan()
        self.by_rel = {n.rel: n for n in self.notes}
        self._index_names()
        for note in self.notes:
            note.links = extract_links(note)
        self.members = self._load_members()
        self.settings = self._load_settings()

    # ---------- scanning ----------
    def _scan(self) -> None:
        for path in sorted(self.root.rglob("*")):
            rel = path.relative_to(self.root).as_posix()
            parts = rel.split("/")
            if any(p in SKIP_DIRS for p in parts[:-1]) or parts[0] in SKIP_DIRS:
                continue
            if not path.is_file():
                continue
            if rel.startswith(TOOLS_DIR):
                continue
            ext = path.suffix.lower().lstrip(".")
            if ext == "md":
                text = path.read_text(encoding="utf-8", errors="replace")
                note = Note(rel=rel, path=path, text=text)
                if rel.startswith(TEMPLATE_DIRS):
                    self.templates.append(note)
                    continue
                try:
                    note.fm = fmlib.parse(text)
                except fmlib.FrontmatterError as exc:
                    note.fm_error = exc
                    note.fm = fmlib.Frontmatter(body=text)
                self.notes.append(note)
            elif path.name in NON_ATTACHMENT_NAMES or ext in NON_ATTACHMENT_EXT \
                    or rel.startswith("Resources/lab_resources/schema/"):
                self.other_files.append(rel)
            else:
                self.attachments.append(rel)

    def _index_names(self) -> None:
        self.by_path_noext: dict[str, list[str]] = {}
        self.by_basename: dict[str, list[str]] = {}
        all_files = [n.rel for n in self.notes] + [t.rel for t in self.templates] + self.attachments + self.other_files
        for rel in all_files:
            low = rel.lower()
            key = low[:-3] if low.endswith(".md") else low
            self.by_path_noext.setdefault(key, []).append(rel)
            base = key.rsplit("/", 1)[-1]
            self.by_basename.setdefault(base, []).append(rel)

    def resolve(self, target: str, from_rel: str = "") -> str | None:
        """Resolve a link target Obsidian-style; returns the vault-relative path or None (cached)."""
        key = (target, from_rel.rsplit("/", 1)[0] if "/" in from_rel else "", from_rel.startswith(EXAMPLES_DIR))
        cache = self.__dict__.setdefault("_resolve_cache", {})
        if key not in cache:
            cache[key] = self._resolve(target, from_rel)
        return cache[key]

    def _resolve(self, target: str, from_rel: str = "") -> str | None:
        t = unquote(target).strip().replace("\\", "/")
        if not t:
            return None
        low = t.lower().lstrip("/")
        if low.endswith(".md"):
            low = low[:-3]
        if low in self.by_path_noext:
            return self.by_path_noext[low][0]
        if from_rel and ("/" in low or low.startswith(".")):
            base_dir = from_rel.rsplit("/", 1)[0] if "/" in from_rel else ""
            joined = _normpath(f"{base_dir}/{low}" if base_dir else low)
            if joined in self.by_path_noext:
                return self.by_path_noext[joined][0]
        if "/" in low:
            suffix = "/" + low
            for key, rels in self.by_path_noext.items():
                if key.endswith(suffix):
                    return rels[0]
            return None
        hits = self.by_basename.get(low)
        if not hits:
            return None
        if len(hits) > 1 and from_rel:
            # prefer a match on the same side of _Examples/ as the linking note
            same = [h for h in hits if h.startswith(EXAMPLES_DIR) == from_rel.startswith(EXAMPLES_DIR)]
            if same:
                return same[0]
        return hits[0]

    # ---------- identity notes ----------
    def _load_members(self) -> list[Member]:
        note = self.by_rel.get(MEMBERS_NOTE)
        if not note:
            return []
        members = []
        for row in parse_table(note.text, required_headers=("name", "initials", "role", "git email", "status")):
            members.append(Member(name=row["name"], initials=row["initials"].upper(),
                                  role=row["role"].lower(), git_email=row["git email"].lower(),
                                  status=row["status"].lower()))
        return members

    def _load_settings(self) -> dict:
        note = self.by_rel.get(SETTINGS_NOTE)
        return dict(note.data) if note else {}

    @property
    def member_initials(self) -> set[str]:
        return {m.initials for m in self.members if m.initials}

    def reviewer_by_name(self, name: str) -> Member | None:
        for m in self.members:
            if m.name.strip().lower() == str(name).strip().lower() and m.is_reviewer:
                return m
        return None

    def max_attachment_bytes(self) -> int:
        mb = self.settings.get("max_attachment_mb") or self.schema.max_attachment_mb
        try:
            return int(float(mb) * 1024 * 1024)
        except (TypeError, ValueError):
            return int(self.schema.max_attachment_mb * 1024 * 1024)

    # ---------- plugins ----------
    def enabled_plugins(self) -> list[str]:
        path = self.root / ".obsidian" / "community-plugins.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def installed_plugins(self) -> dict[str, str]:
        out = {}
        pdir = self.root / ".obsidian" / "plugins"
        if not pdir.is_dir():
            return out
        for d in sorted(pdir.iterdir()):
            manifest = d / "manifest.json"
            if manifest.is_file():
                try:
                    out[d.name] = json.loads(manifest.read_text(encoding="utf-8")).get("version", "")
                except json.JSONDecodeError:
                    out[d.name] = ""
        return out


def _normpath(path: str) -> str:
    parts = []
    for p in path.split("/"):
        if p in ("", "."):
            continue
        if p == "..":
            if parts:
                parts.pop()
            continue
        parts.append(p)
    return "/".join(parts)


def scrub(text: str) -> str:
    """Blank out code fences, inline code, %% comments %% and Templater tags (keep line count)."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = TEMPLATER_RE.sub(blank, text)
    text = COMMENT_RE.sub(blank, text)
    out, in_fence, fence = [], False, ""
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(2)
            if not in_fence:
                in_fence, fence = True, marker[0] * 3
                out.append("")
                continue
            if marker.startswith(fence):
                in_fence = False
                out.append("")
                continue
        if in_fence:
            out.append("")
            continue
        out.append(INLINE_CODE_RE.sub(lambda mm: " " * len(mm.group(0)), line))
    return "\n".join(out)


def extract_links(note: Note) -> list[Link]:
    links: list[Link] = []
    if note.fm:
        for key, value in note.fm.data.items():
            for target in fmlib.link_targets(value):
                links.append(Link(target=target, line=note.line_of(key) or 1, embed=False, source=key))
        body = note.fm.body
        offset = note.fm.body_start_line
    else:
        body, offset = note.text, 1
    for i, line in enumerate(scrub(body).split("\n")):
        for m in WIKI_RE.finditer(line):
            inner = m.group(2)
            target = re.split(r"[|#^]", inner, maxsplit=1)[0].strip().rstrip("\\").strip()
            if target:
                links.append(Link(target=target, line=offset + i, embed=bool(m.group(1)), source="body"))
        for m in MD_LINK_RE.finditer(line):
            url = m.group(2)
            if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("#"):
                continue
            target = url.split("#", 1)[0]
            if target:
                links.append(Link(target=target, line=offset + i, embed=bool(m.group(1)), source="body"))
    return links


def parse_table(text: str, required_headers: tuple, heading: str | None = None) -> list[dict]:
    """Rows of the first Markdown table (optionally under `heading`) whose header contains
    `required_headers` (case-insensitive). Values are stripped strings."""
    lines = text.split("\n")
    start = 0
    if heading:
        for i, ln in enumerate(lines):
            if ln.strip().lower() == heading.lower():
                start = i + 1
                break
        else:
            return []
    i = start
    while i < len(lines):
        ln = lines[i].strip()
        if heading and ln.startswith("#") and i > start:
            return []
        if ln.startswith("|"):
            header = [c.strip().lower() for c in ln.strip("|").split("|")]
            if all(h in header for h in required_headers):
                rows = []
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith("|"):
                    cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    if not all(set(c) <= set("-: ") for c in cells):
                        rows.append(dict(zip(header, cells + [""] * (len(header) - len(cells)))))
                    j += 1
                return rows
        i += 1
    return []
