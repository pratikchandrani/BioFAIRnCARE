"""EX rules: example content stays inside _Examples/ and nothing real depends on it."""

from __future__ import annotations

from ..vault import EXAMPLES_DIR
from . import finding


def ex001(ctx):
    for note in ctx.vault.notes:
        flagged = note.data.get("example") is True
        if note.is_example and note.type and not flagged:
            yield finding("EX001", "error", note, "note in _Examples/ must have 'example: true'", 1)
        elif not note.is_example and flagged:
            yield finding("EX001", "error", note, "'example: true' note must live in _Examples/", note.line_of("example"))


def ex002(ctx):
    v = ctx.vault
    for note in v.notes:
        if note.is_example:
            continue
        for link in note.links:
            target = v.resolve(link.target, note.rel)
            if target and target.startswith(EXAMPLES_DIR):
                yield finding("EX002", "error", note,
                              f"links into _Examples/ ([[{link.target}]]); this breaks when examples are deleted",
                              link.line)


RULES = {"EX001": ex001, "EX002": ex002}
