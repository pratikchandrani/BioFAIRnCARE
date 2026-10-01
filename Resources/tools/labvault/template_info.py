"""Parser for TEMPLATE-INFO blocks (contracts/template-info.md)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

START = "/* TEMPLATE-INFO"
END = "END TEMPLATE-INFO */"
KEYS = [
    "template_id", "name", "category", "version", "status", "lab_owned",
    "original_author", "original_date", "source_release",
    "base_template_id", "base_version", "customised_by", "customised_on",
    "customisation_summary",
]
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
LOCAL_RE = re.compile(r"^(\d+\.\d+\.\d+)-local\.(\d+)$")


class TemplateInfoError(ValueError):
    def __init__(self, message: str, line: int | None = None):
        super().__init__(message)
        self.line = line


@dataclass
class TemplateInfo:
    fields: dict = field(default_factory=dict)
    changelog: list = field(default_factory=list)  # list of dicts: version, date, author, summary
    end_offset: int = 0  # character offset just after the closing "-%>" (or END marker)
    start_line: int = 1

    def get(self, key, default=None):
        value = self.fields.get(key)
        return default if value in (None, "") else value

    @property
    def is_local(self) -> bool:
        return str(self.fields.get("lab_owned", "")).lower() == "false"


def parse(text: str) -> TemplateInfo:
    start = text.find(START)
    if start == -1:
        raise TemplateInfoError("no TEMPLATE-INFO block found")
    prefix = text[:start]
    if prefix.strip() not in ("<%*", ""):
        raise TemplateInfoError("TEMPLATE-INFO must be the first thing in the file (inside '<%*')")
    end = text.find(END, start)
    if end == -1:
        raise TemplateInfoError("TEMPLATE-INFO block is not closed with 'END TEMPLATE-INFO */'")
    inner = text[start + len(START):end]
    if "*/" in inner:
        raise TemplateInfoError("'*/' must not appear inside the TEMPLATE-INFO block")
    start_line = text.count("\n", 0, start) + 1
    info = TemplateInfo(start_line=start_line)
    lines = inner.split("\n")
    in_changelog = False
    header = None
    for offset, raw in enumerate(lines):
        line = raw.strip()
        lineno = start_line + offset
        if not line:
            continue
        if line == "CHANGELOG":
            in_changelog = True
            continue
        if in_changelog:
            if not line.startswith("|"):
                raise TemplateInfoError("CHANGELOG rows must be table rows", lineno)
            cells = [c.strip() for c in line.strip("|").split("|")]
            if header is None:
                header = [c.lower() for c in cells]
                if header[:4] != ["version", "date", "author", "summary"]:
                    raise TemplateInfoError("CHANGELOG header must be | version | date | author | summary |", lineno)
                continue
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if len(cells) < 4:
                raise TemplateInfoError("CHANGELOG row needs 4 cells", lineno)
            info.changelog.append(dict(zip(["version", "date", "author", "summary"], cells[:4])))
            continue
        if ":" not in line:
            raise TemplateInfoError(f"expected 'key: value', got {line[:40]!r}", lineno)
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in KEYS:
            raise TemplateInfoError(f"unknown TEMPLATE-INFO key '{key}'", lineno)
        info.fields[key] = value.strip()
    for required in ("template_id", "name", "category", "version", "status", "lab_owned",
                     "original_author", "original_date", "source_release"):
        if not info.fields.get(required):
            raise TemplateInfoError(f"TEMPLATE-INFO is missing '{required}'")
    if not info.changelog:
        raise TemplateInfoError("TEMPLATE-INFO has no CHANGELOG rows")
    close = text.find("%>", end)
    info.end_offset = close + 2 if close != -1 else end + len(END)
    return info


def body_after(text: str, info: TemplateInfo) -> str:
    """Template text after the TEMPLATE-INFO execution block (the note skeleton)."""
    rest = text[info.end_offset:]
    return rest[1:] if rest.startswith("\n") else rest


def version_key(version: str) -> tuple:
    base = LOCAL_RE.match(version)
    core = base.group(1) if base else version
    local = int(base.group(2)) if base else 0
    try:
        return tuple(int(x) for x in core.split(".")) + (local,)
    except ValueError:
        return (0, 0, 0, 0)
