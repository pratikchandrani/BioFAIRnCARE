"""OK rules: Open Knowledge Format (OKF v0.2) conformance (contracts: specs/005 okf-rules.md)."""

from __future__ import annotations

from ..frontmatter import is_empty
from ..okf import is_exempt
from . import finding


def ok001(ctx):
    for note in ctx.vault.notes:
        if note.fm_error is not None or is_exempt(ctx.schema, note.rel):
            continue  # unparseable frontmatter is FM001
        if not note.fm.present:
            yield finding("OK001", "error", note, "no properties (frontmatter): OKF needs a 'type'", 1,
                          "add properties with a 'type' (create the note from the matching template)")
        elif is_empty(note.type):
            yield finding("OK001", "error", note, "'type' is empty: OKF needs a non-empty 'type'", 1)


def ok002(ctx):
    reserved = {n.lower() for n in ctx.schema.okf.get("reserved_names", ["index.md", "log.md"])}
    v = ctx.vault
    for rel in [n.rel for n in v.notes] + [t.rel for t in v.templates]:
        if rel.rsplit("/", 1)[-1].lower() in reserved:
            yield finding("OK002", "error", rel, "file name reserved by OKF (index.md / log.md)", None,
                          "rename it — these names are reserved for OKF exports")


def ok003(ctx):
    limit = int(ctx.schema.okf.get("description_max", 200))
    for note in ctx.typed_notes():
        data = note.data
        if is_empty(data.get("title")):
            yield finding("OK003", "info", note, "no 'title' (OKF recommended field)", note.line_of("type"))
        desc = data.get("description")
        if note.type != "daily" and is_empty(desc):
            yield finding("OK003", "info", note, "no 'description' (OKF recommended field)", note.line_of("type"),
                          "add a one-sentence description")
        elif isinstance(desc, str) and len(desc) > limit:
            yield finding("OK003", "info", note, f"'description' longer than {limit} characters",
                          note.line_of("description"), "shorten it to one sentence")


def ok004(ctx):
    finished = set(ctx.schema.okf.get("finished_experiment_statuses", ["completed"]))
    for note in ctx.typed_notes():
        if note.type == "experiment" and note.data.get("status") in finished and is_empty(note.data.get("description")):
            yield finding("OK004", "warning", note,
                          f"{note.data.get('status')} experiment without a 'description'",
                          note.line_of("status"), "describe what was done and found in one sentence")


RULES = {"OK001": ok001, "OK002": ok002, "OK003": ok003, "OK004": ok004}
