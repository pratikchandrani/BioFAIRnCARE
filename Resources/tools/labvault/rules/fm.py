"""FM rules: frontmatter shape and schema conformance."""

from __future__ import annotations

import re

from ..frontmatter import is_empty
from . import conditional_findings, finding

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?)?$")


def fm001(ctx):
    for note in ctx.vault.notes:
        if note.fm_error is not None:
            yield finding("FM001", "error", note, f"frontmatter outside supported YAML subset: {note.fm_error}",
                          note.fm_error.line)


def fm002(ctx):
    core = ctx.schema.core_required
    for note in ctx.typed_notes():
        missing = [k for k in core if is_empty(note.data.get(k))]
        if missing:
            yield finding("FM002", "error", note, "missing core properties: " + ", ".join(missing), 1)


def fm003(ctx):
    for note in ctx.typed_notes():
        tdef = ctx.schema.type_def(note.type)
        if not tdef:
            continue
        missing = [k for k in tdef.get("required", []) if is_empty(note.data.get(k))]
        missing_keys = [k for k in tdef.get("required_keys", []) if k not in note.data]
        if missing:
            yield finding("FM003", "error", note, f"missing required '{note.type}' properties: " + ", ".join(missing), 1)
        if missing_keys:
            yield finding("FM003", "error", note,
                          f"missing '{note.type}' property keys (may be empty): " + ", ".join(missing_keys), 1)
    yield from conditional_findings(ctx, "FM003")


def fm004(ctx):
    schema = ctx.schema
    for note in ctx.typed_notes():
        tdef = schema.type_def(note.type)
        if tdef is None:
            yield finding("FM004", "error", note, f"unknown note type '{note.type}' (allowed: {', '.join(schema.types)})",
                          note.line_of("type"))
            continue
        status = note.data.get("status")
        if not is_empty(status) and status not in tdef.get("status", []):
            yield finding("FM004", "error", note,
                          f"status '{status}' not allowed for {note.type} (allowed: {', '.join(tdef['status'])})",
                          note.line_of("status"))
        for key, allowed in schema.enums.items():
            value = note.data.get(key)
            if is_empty(value):
                continue
            values = value if isinstance(value, list) else [value]
            for v in values:
                if v not in allowed:
                    yield finding("FM004", "error", note, f"'{key}' value '{v}' not allowed (allowed: {', '.join(allowed)})",
                                  note.line_of(key))
        for key in ("ai_assisted", "example", "lab_owned", "review_requested", "human_or_community_data", "animal_study"):
            if key in note.data and note.data[key] is not None and not isinstance(note.data[key], bool):
                yield finding("FM004", "error", note, f"'{key}' must be true or false", note.line_of(key))


def fm005(ctx):
    for note in ctx.typed_notes():
        for key in ctx.schema.date_fields:
            value = note.data.get(key)
            if is_empty(value):
                continue
            if not isinstance(value, str) or not DATE_RE.match(value):
                yield finding("FM005", "error", note, f"'{key}' must be an ISO 8601 date (YYYY-MM-DD), got {value!r}",
                              note.line_of(key))


RULES = {"FM001": fm001, "FM002": fm002, "FM003": fm003, "FM004": fm004, "FM005": fm005}
