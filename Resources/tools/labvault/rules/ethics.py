"""AN / BS rules: animal ethics and biosafety fields."""

from __future__ import annotations

from . import conditional_findings


def an001(ctx):
    yield from conditional_findings(ctx, "AN001")


def bs001(ctx):
    yield from conditional_findings(ctx, "BS001")


RULES = {"AN001": an001, "BS001": bs001}
