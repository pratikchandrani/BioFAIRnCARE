"""Loader for Resources/lab_resources/schema/note-types.json (contracts/note-schema.md)."""

from __future__ import annotations

import json
import re
from pathlib import Path

SCHEMA_PATH = "Resources/lab_resources/schema/note-types.json"


class SchemaError(Exception):
    pass


class Schema:
    def __init__(self, raw: dict):
        self.raw = raw
        try:
            self.version = raw["schema_version"]
            self.edition = raw.get("edition", "standard")
            self.types = raw["types"]
            self.core_required = raw["core_required"]
            self.groups = raw["groups"]
            self.enums = raw["enums"]
            self.date_fields = set(raw["date_fields"])
            self.id_patterns = {k: re.compile(v) for k, v in raw["id_patterns"].items()}
            self.attachment_name = re.compile(raw["attachment_name_pattern"])
        except KeyError as exc:
            raise SchemaError(f"schema is missing key {exc}") from exc
        self.max_attachment_mb = raw.get("max_attachment_mb", 10)
        self.open_ext = set(raw.get("open_attachment_extensions", []))
        self.raw_ext = set(raw.get("raw_extensions_disallowed", []))
        self.untyped_allowed = set(raw.get("untyped_allowed", []))
        self.link_property_types = raw.get("link_property_types", {})
        self.common_conditional = raw.get("common_conditional", [])
        self.catalogue = raw.get("catalogue", [])
        self.okf = raw.get("okf", {})
        self.removed_plugin_terms = raw.get("removed_plugin_terms", {})
        self.removed_plugin_exempt = set(raw.get("removed_plugin_exempt_files", []))

    def type_def(self, note_type: str) -> dict | None:
        return self.types.get(note_type)

    def conditionals(self, note_type: str) -> list[dict]:
        tdef = self.types.get(note_type) or {}
        return list(self.common_conditional) + list(tdef.get("conditional", []))


def load(vault_root: Path) -> Schema:
    path = vault_root / SCHEMA_PATH
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SchemaError(f"schema file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SchemaError(f"schema file is not valid JSON: {exc}") from exc
    return Schema(raw)


def condition_matches(when: dict, data: dict) -> bool:
    """`when` maps property -> allowed values; empty `when` always matches."""
    for key, allowed in when.items():
        if data.get(key) not in allowed:
            return False
    return True
