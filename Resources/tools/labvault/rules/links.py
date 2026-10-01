"""LK rules: unresolved links, orphans, typed link properties."""

from __future__ import annotations

from ..frontmatter import link_targets
from . import finding

ORPHAN_EXEMPT_TYPES = {"daily", "index", "settings"}
ORPHAN_EXEMPT_FILES = {"Home.md", "README.md", "CHANGELOG.md", "UPGRADE.md"}


def lk001(ctx):
    v = ctx.vault
    for note in v.notes:
        for link in note.links:
            if v.resolve(link.target, note.rel) is None:
                yield finding("LK001", "error", note, f"unresolved link [[{link.target}]]", link.line)


def lk002(ctx):
    v = ctx.vault
    inbound = set()
    for note in v.notes:
        for link in note.links:
            target = v.resolve(link.target, note.rel)
            if target and target != note.rel:
                inbound.add(target)
    include_examples = getattr(ctx.options, "include_examples", False)
    for note in v.notes:
        if note.rel in inbound or note.rel in ORPHAN_EXEMPT_FILES or note.rel in ctx.schema.untyped_allowed:
            continue
        if note.type in ORPHAN_EXEMPT_TYPES or note.stem == "_Index":
            continue
        if note.is_example and not include_examples:
            continue
        yield finding("LK002", "warning", note, "orphan note: nothing links to it",
                      suggestion="link it from a daily note, project or index")


def lk003(ctx):
    v = ctx.vault
    expected_types = ctx.schema.link_property_types
    for note in ctx.typed_notes():
        for prop, expected in expected_types.items():
            for target in link_targets(note.data.get(prop)):
                rel = v.resolve(target, note.rel)
                tnote = v.by_rel.get(rel) if rel else None
                if tnote is not None and tnote.type and tnote.type != expected:
                    yield finding("LK003", "error", note,
                                  f"'{prop}' links to [[{target}]] which is a {tnote.type}, expected {expected}",
                                  note.line_of(prop))


def lk004(ctx):
    """Every experiment must be traceable to a daily note (link in either direction)."""
    v = ctx.vault
    daily = {n.rel for n in v.notes if n.type == "daily"}
    linked = set()
    for note in v.notes:
        for link in note.links:
            target = v.resolve(link.target, note.rel)
            if not target:
                continue
            if note.rel in daily:
                linked.add(target)
            elif target in daily:
                linked.add(note.rel)
    for note in ctx.typed_notes():
        if note.type == "experiment" and note.rel not in linked:
            yield finding("LK004", "warning", note, "experiment is not linked from or to any daily note (traceability)",
                          suggestion="add '- Performed [[<this note>]]' to the daily note of the day the work was done")


RULES = {"LK001": lk001, "LK002": lk002, "LK003": lk003, "LK004": lk004}
