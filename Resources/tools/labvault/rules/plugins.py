"""PL rules: plugin register matches installed/enabled plugins; removed plugins not referenced."""

from __future__ import annotations

import json
import re

from ..vault import PLUGIN_REGISTER, parse_table
from . import finding

HEADERS = ("plugin id", "version", "default state")


def register_rows(ctx) -> list[dict] | None:
    note = ctx.vault.by_rel.get(PLUGIN_REGISTER)
    if note is None:
        return None
    return parse_table(note.text, HEADERS, heading="## Registered plugins")


def pl001(ctx):
    rows = register_rows(ctx)
    if rows is None:
        yield finding("PL001", "error", PLUGIN_REGISTER, "plugin register note is missing")
        return
    registered_enabled = {r["plugin id"].strip("`") for r in rows if r["default state"].lower() == "enabled"}
    enabled = set(ctx.vault.enabled_plugins())
    for pid in sorted(enabled - registered_enabled):
        yield finding("PL001", "error", ".obsidian/community-plugins.json",
                      f"plugin '{pid}' is enabled but not registered with default state 'enabled'")
    for pid in sorted(registered_enabled - enabled):
        yield finding("PL001", "error", PLUGIN_REGISTER, f"plugin '{pid}' is registered as enabled but not enabled")


def pl002(ctx):
    rows = register_rows(ctx)
    if rows is None:
        return
    registered = {r["plugin id"].strip("`"): r for r in rows}
    installed = ctx.vault.installed_plugins()
    for pid in sorted(set(installed) - set(registered)):
        yield finding("PL002", "error", f".obsidian/plugins/{pid}", f"installed plugin '{pid}' is not in the register")
    for pid in sorted(set(registered) - set(installed)):
        yield finding("PL002", "error", PLUGIN_REGISTER, f"registered plugin '{pid}' is not installed")
    for pid in sorted(set(registered) & set(installed)):
        reg_v = registered[pid]["version"].strip("`")
        if reg_v and installed[pid] and reg_v != installed[pid]:
            yield finding("PL002", "error", PLUGIN_REGISTER,
                          f"register says {pid} {reg_v} but installed version is {installed[pid]}")


def pl003(ctx):
    terms = ctx.schema.removed_plugin_terms
    exempt = ctx.schema.removed_plugin_exempt
    checks = []
    for note in ctx.vault.notes:
        # only lab-owned notes (guides, Home, registers, indexes); students may mention anything
        if note.rel not in exempt and (note.data.get("lab_owned") is True or note.rel == "Home.md"):
            checks.append((note.rel, note.text))
    root = ctx.vault.root / ".obsidian"
    for path in list((root / "snippets").glob("*.css")) + [root / "hotkeys.json", root / "appearance.json",
                                                            root / "community-plugins.json"]:
        if path.is_file():
            checks.append((path.relative_to(ctx.vault.root).as_posix(), path.read_text(encoding="utf-8")))
    for t in ctx.vault.templates:
        checks.append((t.rel, t.text))
    for rel, text in checks:
        for pid, words in terms.items():
            for w in words:
                for m in re.finditer(re.escape(w), text):
                    line = text.count("\n", 0, m.start()) + 1
                    yield finding("PL003", "error", rel, f"references removed plugin '{pid}' ({w!r})", line)
                    break


RULES = {"PL001": pl001, "PL002": pl002, "PL003": pl003}
