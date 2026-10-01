"""Rule registry. Each rule module exposes RULES = {rule_id: function(ctx) -> iterable[Finding]}."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass

from ..frontmatter import is_empty
from ..schema import condition_matches
from ..vault import Finding, Note, Vault


@dataclass
class Context:
    vault: Vault
    options: object
    git: object  # gitcheck.Git or None

    @property
    def schema(self):
        return self.vault.schema

    def typed_notes(self, include_examples: bool = True):
        for n in self.vault.notes:
            if n.fm_error is None and n.type and (include_examples or not n.is_example):
                yield n


def finding(rule, severity, note_or_path, message, line=None, suggestion=None) -> Finding:
    path = note_or_path.rel if isinstance(note_or_path, Note) else note_or_path
    return Finding(rule=rule, severity=severity, path=path, message=message, line=line, suggestion=suggestion)


def conditional_findings(ctx: Context, rule_id: str, severity: str = "error"):
    """Evaluate schema conditionals tagged with `rule_id` for every typed note."""
    schema = ctx.schema
    for note in ctx.typed_notes():
        data = note.data
        for cond in schema.conditionals(note.type):
            if cond.get("rule", "FM003") != rule_id:
                continue
            if not condition_matches(cond.get("when", {}), data):
                continue
            missing = []
            for key in cond.get("require", []):
                if is_empty(data.get(key)):
                    missing.append(key)
            group = cond.get("require_group")
            if group:
                missing += [k for k in schema.groups.get(group, []) if is_empty(data.get(k))]
            any_of = cond.get("require_any")
            if any_of and all(is_empty(data.get(k)) for k in any_of):
                missing.append(" or ".join(any_of))
            for key, expected in cond.get("equals", {}).items():
                if data.get(key) != expected:
                    yield finding(rule_id, severity, note,
                                  f"'{key}' must be {str(expected).lower()} for this note "
                                  f"({', '.join(f'{k}={data.get(k)}' for k in cond.get('when', {}))})",
                                  note.line_of(key))
            if missing:
                yield finding(rule_id, severity, note,
                              "missing required " + ("group '" + group + "' fields: " if group else "properties: ")
                              + ", ".join(dict.fromkeys(missing)),
                              note.line_of(list(cond.get("when", {}) or ["type"])[0]))


LITE_SKIPPED = ("SO000", "SO001", "SO002", "SO003", "SO004", "PR002")  # no in-vault sign-off in the Lite edition


def all_rules(edition: str = "standard") -> dict:
    from . import (attachments, care, datarefs, ethics, examples, fm, ids, links, okf, plugins,
                   privacy, protocols, signoff, templates)
    registry = {}
    for mod in (fm, ids, links, attachments, datarefs, care, ethics, signoff, protocols,
                templates, plugins, privacy, examples, okf):
        registry.update(mod.RULES)
    if edition == "lite":
        for rule_id in LITE_SKIPPED:
            registry.pop(rule_id, None)
    return dict(sorted(registry.items()))


def select(registry: dict, include: list[str] | None, skip: list[str] | None) -> dict:
    def match(rule_id, patterns):
        return any(fnmatch.fnmatchcase(rule_id, p.strip().upper()) for p in patterns if p.strip())
    out = {}
    for rid, fn in registry.items():
        if include and not match(rid, include):
            continue
        if skip and match(rid, skip):
            continue
        out[rid] = fn
    return out
