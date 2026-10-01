"""Parser for the vault's YAML frontmatter subset (research R8).

Supported: top-level ``key: value`` pairs; plain, single- and double-quoted scalars;
integers, decimals, booleans, null; block lists (``- item``) and flow lists (``[a, "b"]``).
Anything else (nested maps, anchors/aliases, block scalars, tags) raises FrontmatterError
so the validator can report FM001 instead of guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

KEY_RE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_ \-]*?)\s*:(?:\s+(.*))?$")
INT_RE = re.compile(r"^[-+]?\d+$")
FLOAT_RE = re.compile(r"^[-+]?(\d+\.\d*|\.\d+)([eE][-+]?\d+)?$")
BOOLS = {"true": True, "false": False}
NULLS = {"", "~", "null", "Null", "NULL"}


class FrontmatterError(ValueError):
    def __init__(self, message: str, line: int):
        super().__init__(message)
        self.line = line


@dataclass
class Frontmatter:
    data: dict = field(default_factory=dict)
    lines: dict = field(default_factory=dict)  # key -> 1-based line number in the file
    body: str = ""
    body_start_line: int = 1  # 1-based line where the body starts
    present: bool = False


def split(text: str) -> tuple[list[str] | None, str, int]:
    """Return (frontmatter lines or None, body, body start line)."""
    text = text.lstrip("\ufeff")
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != "---":
        return None, text, 1
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r") in ("---", "..."):
            fm = [ln.rstrip("\r") for ln in lines[1:i]]
            return fm, "\n".join(lines[i + 1:]), i + 2
    raise FrontmatterError("frontmatter opened with '---' but never closed", 1)


def parse(text: str) -> Frontmatter:
    fm_lines, body, body_start = split(text)
    result = Frontmatter(body=body, body_start_line=body_start)
    if fm_lines is None:
        return result
    result.present = True
    current_list_key = None
    bare_keys = set()  # keys written as "key:" with nothing after the colon
    for idx, raw in enumerate(fm_lines):
        lineno = idx + 2
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t" or raw.startswith("- "):
            stripped = raw.strip()
            if current_list_key is not None and (stripped == "-" or stripped.startswith("- ")):
                item_text = stripped[1:].strip()
                if KEY_RE.match(item_text) and not _is_quoted(item_text):
                    raise FrontmatterError(f"nested map inside list '{current_list_key}'", lineno)
                result.data[current_list_key].append(_scalar(item_text, lineno))
                continue
            raise FrontmatterError("indented line is not a list item (nested maps are not supported)", lineno)
        m = KEY_RE.match(raw)
        if not m:
            raise FrontmatterError(f"cannot parse line: {raw.strip()[:40]!r}", lineno)
        key, value = m.group(1).strip(), (m.group(2) or "").strip()
        if key in result.data:
            raise FrontmatterError(f"duplicate key '{key}'", lineno)
        result.lines[key] = lineno
        current_list_key = None
        if value == "":
            result.data[key] = []  # becomes a list if items follow, else normalised below
            bare_keys.add(key)
            current_list_key = key
            continue
        result.data[key] = _value(value, lineno)
    for key in bare_keys:
        if result.data[key] == []:
            result.data[key] = None
    return result


def _is_quoted(text: str) -> bool:
    return len(text) >= 2 and text[0] in "'\"" and text[-1] == text[0]


def _value(text: str, lineno: int):
    if text[0] in "|>":
        raise FrontmatterError("block scalars (| or >) are not supported", lineno)
    if text[0] in "&*!":
        raise FrontmatterError("anchors, aliases and tags are not supported", lineno)
    if text.startswith("{"):
        raise FrontmatterError("flow maps are not supported", lineno)
    if text.startswith("[["):
        raise FrontmatterError("wikilinks in properties must be quoted, e.g. \"[[Note]]\"", lineno)
    if text.startswith("["):
        if not text.endswith("]"):
            raise FrontmatterError("unterminated flow list", lineno)
        return [_scalar(item, lineno) for item in _split_flow(text[1:-1], lineno)]
    return _scalar(text, lineno)


def _split_flow(inner: str, lineno: int) -> list[str]:
    items, buf, quote = [], [], None
    i = 0
    while i < len(inner):
        ch = inner[i]
        if quote:
            buf.append(ch)
            if ch == "\\" and quote == '"' and i + 1 < len(inner):
                buf.append(inner[i + 1])
                i += 1
            elif ch == quote:
                if quote == "'" and i + 1 < len(inner) and inner[i + 1] == "'":
                    buf.append("'")
                    i += 1
                else:
                    quote = None
        elif ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            items.append("".join(buf).strip())
            buf = []
        elif ch in "[]{}":
            raise FrontmatterError("nested collections are not supported", lineno)
        else:
            buf.append(ch)
        i += 1
    if quote:
        raise FrontmatterError("unterminated quoted string in list", lineno)
    last = "".join(buf).strip()
    if last or items:
        items.append(last)
    return [it for it in items if it != ""]


def _scalar(text: str, lineno: int):
    text = text.strip()
    if text == "":
        return None
    if text[0] == '"':
        if len(text) < 2 or not text.endswith('"'):
            raise FrontmatterError("unterminated double-quoted string", lineno)
        return _unescape_double(text[1:-1], lineno)
    if text[0] == "'":
        if len(text) < 2 or not text.endswith("'"):
            raise FrontmatterError("unterminated single-quoted string", lineno)
        return text[1:-1].replace("''", "'")
    if text[0] in "&*!|>{":
        raise FrontmatterError("unsupported YAML construct", lineno)
    if " #" in text:
        text = text.split(" #", 1)[0].rstrip()
    if text in NULLS:
        return None
    if text in BOOLS:
        return BOOLS[text]
    if INT_RE.match(text) and not (len(text.lstrip("+-")) > 1 and text.lstrip("+-").startswith("0")):
        return int(text)
    if FLOAT_RE.match(text):
        return float(text)
    if ": " in text:
        raise FrontmatterError("unquoted value contains ': ' (quote the value)", lineno)
    return text


_ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "/": "/", "0": "\0"}


def _unescape_double(s: str, lineno: int) -> str:
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\":
            if i + 1 >= len(s):
                raise FrontmatterError("dangling backslash in quoted string", lineno)
            nxt = s[i + 1]
            if nxt not in _ESCAPES:
                raise FrontmatterError(f"unsupported escape \\{nxt}", lineno)
            out.append(_ESCAPES[nxt])
            i += 2
            continue
        if ch == '"':
            raise FrontmatterError("unescaped double quote inside string", lineno)
        out.append(ch)
        i += 1
    return "".join(out)


WIKILINK_RE = re.compile(r"\[\[([^\[\]|#^]+)(?:[#^][^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")


def link_targets(value) -> list[str]:
    """Wikilink targets contained in a property value (string or list)."""
    values = value if isinstance(value, list) else [value]
    out = []
    for v in values:
        if isinstance(v, str):
            out.extend(m.group(1).strip() for m in WIKILINK_RE.finditer(v))
    return out


def is_empty(value) -> bool:
    return value is None or value == "" or value == []
