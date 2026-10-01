"""CA rules: CARE fields for human- or community-derived material."""

from __future__ import annotations

from . import conditional_findings, finding


def ca001(ctx):
    yield from conditional_findings(ctx, "CA001")


def ca002(ctx):
    yield from conditional_findings(ctx, "CA002", severity="warning")
    for note in ctx.typed_notes():
        if note.type == "experiment" and note.data.get("source_kind") == "human" \
                and note.data.get("human_or_community_data") is not True:
            yield finding("CA002", "warning", note, "human source but 'human_or_community_data' is not true",
                          note.line_of("human_or_community_data"))


RULES = {"CA001": ca001, "CA002": ca002}
