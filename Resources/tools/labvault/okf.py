"""Open Knowledge Format (OKF v0.2) helpers shared by the validator rules and okf_export.py.

OKF: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
The vault keeps wikilinks and the lab `status`; this module maps them to OKF for the export
(constitution v2.3.0, Principle VII) and checks bundle conformance.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

from . import frontmatter as fmlib
from .vault import COMMENT_RE, FENCE_RE, INLINE_CODE_RE, Vault

OKF_VERSION = "0.2"
IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "svg", "webp"}
DEFAULT_STATUS = "stable"
DYNAMIC_LANGS = {"dataview", "dataviewjs", "tasks", "base", "query", "kanban"}
DYNAMIC_NOTE = "> Dynamic view in the original vault (not exported)."
REMOVED_LINK = "(link removed)"
WIKI_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
MD_LINK_RE = re.compile(r"(!?)\[([^\]\n]*)\]\(([^)\s]+)\)")
INLINE_DV_RE = re.compile(r"`\$?=[^`\n]*`")
DATE_HEADING_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")


# ---------------------------------------------------------------- mapping
def okf_status(schema, note_type: str | None, lab_status) -> str:
    table = (schema.okf.get("status_map") or {}).get(note_type or "", {})
    return table.get(str(lab_status), DEFAULT_STATUS) if lab_status is not None else DEFAULT_STATUS


def is_exempt(schema, rel: str) -> bool:
    return rel.startswith(tuple(schema.okf.get("exempt_prefixes", ())))


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "unknown"


ID_INITIALS_RE = re.compile(r"^[A-Z]+-([A-Z]{2,4})-\d{8}-\d{2}$")


def actor(vault: Vault, name, record_id=None) -> str:
    """OKF actor id (§7) for a person named in the vault: human:<initials> when known.

    Initials come from Lab members, then Vault settings, then the owner's initials embedded in a
    lab record id (`EXP-PC-20261002-01` -> PC); otherwise a slug of the name."""
    name = str(name or "").strip()
    if not name:
        return "human:unknown"
    for m in vault.members:
        if m.name.strip().lower() == name.lower() and m.initials:
            return f"human:{m.initials}"
    settings = vault.settings
    if str(settings.get("owner", "")).strip().lower() == name.lower() and settings.get("owner_initials"):
        return f"human:{str(settings['owner_initials']).upper()}"
    m = ID_INITIALS_RE.match(str(record_id or ""))
    if m:
        return f"human:{m.group(1)}"
    return f"human:{slug(name)}"


def bundle_link(rel: str, anchor: str = "") -> str:
    return "/" + quote(rel, safe="/") + (f"#{anchor}" if anchor else "")


def heading_anchor(heading: str) -> str:
    text = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return re.sub(r"\s+", "-", text)


# ---------------------------------------------------------------- body transforms
def strip_comments(text: str) -> str:
    return COMMENT_RE.sub("", text)


def replace_dynamic_blocks(text: str) -> str:
    """Replace Dataview / Tasks / Bases fenced blocks and inline queries with a short note."""
    out, fence, dynamic = [], None, False
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group(2)[0] * 3
            lang = line.strip()[len(m.group(2)):].strip().split(" ")[0].lower()
            dynamic = lang in DYNAMIC_LANGS
            out.append(DYNAMIC_NOTE if dynamic else line)
            continue
        if fence is not None:
            if m and m.group(2).startswith(fence):
                fence = None
                if not dynamic:
                    out.append(line)
                dynamic = False
                continue
            if not dynamic:
                out.append(line)
            continue
        out.append(INLINE_DV_RE.sub("(dynamic value)", line))
    return "\n".join(out)


def _split_code(line: str):
    """Yield (is_code, segment) pieces of a line around inline code spans."""
    pos = 0
    for m in INLINE_CODE_RE.finditer(line):
        if m.start() > pos:
            yield False, line[pos:m.start()]
        yield True, m.group(0)
        pos = m.end()
    if pos < len(line):
        yield False, line[pos:]


class LinkConverter:
    """Convert wikilinks / relative Markdown links of one note to OKF bundle-relative links.

    `included` maps vault rel -> bundle rel for exported notes; `copied` is the set of copied
    attachment rels. Links to anything else never reveal the target's name (research R7).
    """

    def __init__(self, vault: Vault, included: dict[str, str], copied: set[str]):
        self.vault = vault
        self.included = included
        self.copied = copied

    def _target(self, raw: str, from_rel: str):
        target = raw.strip().rstrip("\\").strip()
        if not target:
            return from_rel
        return self.vault.resolve(target, from_rel)

    def wikilink(self, embed: str, inner: str, from_rel: str) -> str:
        alias = None
        if "|" in inner:
            inner, alias = inner.split("|", 1)
            alias = alias.strip()
        anchor = ""
        target = inner
        if "#" in inner:
            target, heading = inner.split("#", 1)
            anchor = "" if heading.startswith("^") else heading_anchor(heading.split("#")[-1])
        if "^" in target:
            target = target.split("^", 1)[0]
        rel = self._target(target, from_rel)
        if rel is None:  # missing note: nothing to protect, keep the author's text
            return alias or inner.strip()
        if rel in self.included:
            text = alias or self.vault.by_rel[rel].data.get("title") or Path(rel).stem
            return f"[{text}]({bundle_link(self.included[rel], anchor)})"
        if rel in self.copied:
            name = alias or Path(rel).name
            bang = "!" if embed and Path(rel).suffix.lower().lstrip(".") in IMAGE_EXT else ""
            return f"{bang}[{name}]({bundle_link(rel)})"
        return alias or REMOVED_LINK

    def mdlink(self, embed: str, text: str, url: str, from_rel: str) -> str:
        if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("#"):
            return f"{embed}[{text}]({url})"
        path, _, anchor = url.partition("#")
        rel = self._target(path, from_rel)
        if rel is None:
            return text or path
        if rel in self.included:
            return f"[{text}]({bundle_link(self.included[rel], anchor)})"
        if rel in self.copied:
            return f"{embed}[{text}]({bundle_link(rel)})"
        return text if text and Path(rel).stem.lower() not in text.lower() else REMOVED_LINK

    def body(self, text: str, from_rel: str) -> str:
        out, fence = [], None
        for line in text.split("\n"):
            m = FENCE_RE.match(line)
            if m:
                if fence is None:
                    fence = m.group(2)[0] * 3
                elif m.group(2).startswith(fence):
                    fence = None
                out.append(line)
                continue
            if fence is not None:
                out.append(line)
                continue
            pieces = []
            for is_code, seg in _split_code(line):
                if not is_code:
                    seg = WIKI_RE.sub(lambda mm: self.wikilink(mm.group(1), mm.group(2), from_rel), seg)
                    seg = MD_LINK_RE.sub(lambda mm: self.mdlink(mm.group(1), mm.group(2), mm.group(3), from_rel), seg)
                pieces.append(seg)
            out.append("".join(pieces))
        return "\n".join(out)

    def value(self, value, from_rel: str):
        """Property value: wikilinks become bundle paths; links to non-exported notes are dropped."""
        if isinstance(value, list):
            items = [self.value(v, from_rel) for v in value]
            return [v for v in items if v is not None]
        if isinstance(value, str) and fmlib.link_targets(value):
            targets = fmlib.link_targets(value)
            rel = self._target(targets[0], from_rel)
            if rel in self.included:
                return bundle_link(self.included[rel])
            if rel in self.copied:
                return bundle_link(rel)
            return None
        return value


# ---------------------------------------------------------------- YAML output
def _scalar(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def dump_yaml(data: dict) -> str:
    """Minimal YAML emitter: scalars, lists of scalars, maps of scalars, lists of maps."""
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            lines += [f"  {k}: {_scalar(v)}" for k, v in value.items()]
        elif isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
                continue
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    first = True
                    for k, v in item.items():
                        lines.append(f"  {'- ' if first else '  '}{k}: {_scalar(v)}")
                        first = False
                else:
                    lines.append(f"  - {_scalar(item)}")
        else:
            lines.append(f"{key}: {_scalar(value)}".rstrip())
    return "---\n" + "\n".join(lines) + "\n---\n"


# ---------------------------------------------------------------- conformance
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_\- ]*?)\s*:(?:\s+(.*))?$")


def read_top_level(text: str) -> dict | None:
    """Top-level keys of a frontmatter block (nested maps tolerated); None if no frontmatter."""
    try:
        fm_lines, _, _ = fmlib.split(text)
    except fmlib.FrontmatterError:
        return None
    if fm_lines is None:
        return None
    out = {}
    for raw in fm_lines:
        if not raw.strip() or raw[0] in " \t-#":
            continue
        m = TOP_KEY_RE.match(raw)
        if m:
            value = (m.group(2) or "").strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            out[m.group(1).strip()] = value
    return out


def check_bundle(out_dir: Path) -> list[str]:
    """The three OKF v0.2 conformance rules (§11); returns a list of problems (empty = conformant)."""
    problems = []
    for path in sorted(out_dir.rglob("*.md")):
        rel = path.relative_to(out_dir).as_posix()
        text = path.read_text(encoding="utf-8")
        name = path.name.lower()
        keys = read_top_level(text)
        if name == "index.md":
            if keys is not None and (rel != "index.md" or set(keys) - {"okf_version"}):
                problems.append(f"{rel}: index.md may only carry okf_version, at the bundle root")
        elif name == "log.md":
            dates = []
            for line in text.split("\n"):
                if line.startswith("## "):
                    m = DATE_HEADING_RE.match(line)
                    if not m:
                        problems.append(f"{rel}: log heading {line!r} is not ## YYYY-MM-DD")
                    else:
                        dates.append(m.group(1))
            if dates != sorted(dates, reverse=True):
                problems.append(f"{rel}: log entries must be newest first")
        else:
            if keys is None:
                problems.append(f"{rel}: no parseable frontmatter")
            elif not keys.get("type"):
                problems.append(f"{rel}: frontmatter has no non-empty 'type'")
    return problems
