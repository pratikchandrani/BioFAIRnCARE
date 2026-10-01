"""Text and JSON reporters (contracts/validator-cli.md)."""

from __future__ import annotations

import json

from . import VALIDATOR_VERSION

ORDER = {"error": 0, "warning": 1, "unverifiable": 2, "info": 3}


def summarise(findings, note_count: int, seconds: float) -> dict:
    counts = {k: 0 for k in ("errors", "warnings", "info", "unverifiable")}
    key = {"error": "errors", "warning": "warnings", "info": "info", "unverifiable": "unverifiable"}
    for f in findings:
        counts[key[f.severity]] += 1
    return {"notes": note_count, **counts, "seconds": round(seconds, 2)}


def sort_findings(findings):
    return sorted(findings, key=lambda f: (ORDER.get(f.severity, 9), f.path, f.line or 0, f.rule))


def as_text(findings, summary: dict) -> str:
    lines = []
    for f in sort_findings(findings):
        loc = f"{f.path}:{f.line}" if f.line else f.path
        line = f"{f.severity.upper():<12} {f.rule} {loc} {f.message}"
        if f.suggestion:
            line += f"  → {f.suggestion}"
        lines.append(line)
    lines.append(f"{summary['errors']} errors, {summary['warnings']} warnings, {summary['info']} info, "
                 f"{summary['unverifiable']} unverifiable in {summary['notes']} notes ({summary['seconds']}s)")
    return "\n".join(lines)


def as_json(findings, summary: dict, vault: str, schema_version: str) -> str:
    return json.dumps({
        "vault": vault,
        "schema_version": schema_version,
        "validator_version": VALIDATOR_VERSION,
        "summary": summary,
        "findings": [f.as_dict() for f in sort_findings(findings)],
    }, indent=2, ensure_ascii=False)
