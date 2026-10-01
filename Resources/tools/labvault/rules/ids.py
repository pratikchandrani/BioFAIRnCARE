"""ID rules: identifier pattern, uniqueness, initials, file names."""

from __future__ import annotations

from ..frontmatter import is_empty
from . import finding


def _id(note):
    value = note.data.get("id")
    return None if is_empty(value) else str(value)


def id001(ctx):
    pats = ctx.schema.id_patterns
    for note in ctx.typed_notes():
        tdef = ctx.schema.type_def(note.type) or {}
        nid = _id(note)
        if nid is None:
            continue
        kind = tdef.get("id_kind", "slug")
        if kind == "daily" and not pats["daily"].match(nid):
            yield finding("ID001", "error", note, f"daily note id '{nid}' must be YYYY-MM-DD", note.line_of("id"))
        elif kind == "prefixed":
            m = pats["prefixed"].match(nid)
            if not m or m.group(1) != tdef.get("id_prefix"):
                yield finding("ID001", "error", note,
                              f"id '{nid}' must match {tdef.get('id_prefix')}-INI-YYYYMMDD-NN", note.line_of("id"))
        elif kind == "slug" and not pats["slug"].match(nid):
            yield finding("ID001", "error", note, f"id '{nid}' contains unsupported characters", note.line_of("id"))


def id002(ctx):
    seen = {}
    for note in ctx.typed_notes():
        nid = _id(note)
        if nid is None:
            continue
        # examples and real records are checked separately: deleting _Examples/ must not change results
        seen.setdefault((note.is_example, nid), []).append(note)
    for (_, nid), notes in seen.items():
        if len(notes) > 1:
            others = ", ".join(n.rel for n in notes)
            for note in notes:
                yield finding("ID002", "error", note, f"duplicate id '{nid}' ({others})", note.line_of("id"),
                              "renumber the newer note that nothing links to yet")


def id003(ctx):
    initials = ctx.vault.member_initials
    pat = ctx.schema.id_patterns["prefixed"]
    for note in ctx.typed_notes():
        if note.is_example:  # fictional examples use the reserved initials EX; real labs never list them
            continue
        nid = _id(note)
        m = pat.match(nid) if nid else None
        if m and m.group(2) not in initials:
            yield finding("ID003", "error", note,
                          f"initials '{m.group(2)}' in id are not listed in Lab members", note.line_of("id"),
                          "ask the vault maintainer to add your initials to Resources/lab_resources/Lab members.md")


def id004(ctx):
    for note in ctx.typed_notes():
        tdef = ctx.schema.type_def(note.type) or {}
        nid = _id(note)
        if nid is None:
            continue
        kind = tdef.get("id_kind")
        if kind == "daily" and note.stem != nid:
            yield finding("ID004", "warning", note, f"daily note file must be named '{nid}.md'")
        elif note.type == "experiment":
            suffix = "_" + nid[len("EXP-"):]
            if not note.stem.endswith(suffix) or note.stem == suffix:
                title = note.data.get("title") or note.stem
                yield finding("ID004", "warning", note,
                              f"experiment file must be named '<Title>_<INI>-<YYYYMMDD>-<NN>.md' ending with "
                              f"'{suffix}'", suggestion=f"rename to '{title}{suffix}.md'")
        elif kind == "prefixed" and not note.stem.startswith(nid):
            yield finding("ID004", "warning", note, f"file name should start with the id '{nid}'",
                          suggestion=f"rename to '{nid} {note.data.get('title') or note.stem}.md'")


RULES = {"ID001": id001, "ID002": id002, "ID003": id003, "ID004": id004}
