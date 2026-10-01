"""DR rules: data and code references are complete."""

from __future__ import annotations

import re

from ..frontmatter import is_empty
from . import conditional_findings, finding

CHECKSUM_RE = re.compile(r"^(sha256:[0-9a-fA-F]{64}|sha1:[0-9a-fA-F]{40}|md5:[0-9a-fA-F]{32})$")


def dr001(ctx):
    yield from conditional_findings(ctx, "DR001")


def dr002(ctx):
    yield from conditional_findings(ctx, "DR002")


def dr003(ctx):
    for note in ctx.typed_notes():
        if note.type != "data_ref":
            continue
        value = note.data.get("checksum")
        if is_empty(value):
            continue
        value = str(value).strip()
        looks_like_path = "/" in value or "\\" in value or value.lower().endswith((".sha256", ".md5", ".txt"))
        if not CHECKSUM_RE.match(value) and not looks_like_path:
            yield finding("DR003", "warning", note, f"checksum {value!r} is not 'sha256:<hex>', 'md5:<hex>' "
                          "or a path to a checksum manifest", note.line_of("checksum"))


RULES = {"DR001": dr001, "DR002": dr002, "DR003": dr003}
