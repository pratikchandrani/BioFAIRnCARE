#!/usr/bin/env python3
"""Validate a BioFAIRnCARE vault against its schema and FAIR/CARE rules.

Usage:  python Resources/tools/validate_vault.py [VAULT_DIR] [options]
Python 3.10+, standard library only. See Resources/lab_resources/Vault Health.md for the
in-Obsidian subset of these checks.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from labvault import report  # noqa: E402
from labvault.gitcheck import Git  # noqa: E402
from labvault.rules import Context, all_rules, select  # noqa: E402
from labvault.schema import SchemaError, load  # noqa: E402
from labvault.vault import Vault  # noqa: E402


def parse_args(argv):
    default_vault = Path(__file__).resolve().parents[2]
    p = argparse.ArgumentParser(description="Validate a BioFAIRnCARE vault (FAIR, CARE and OKF rules).")
    p.add_argument("vault", nargs="?", default=str(default_vault), help="vault folder (default: this vault)")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--rules", default="", help="only these rule ids/patterns, comma-separated (e.g. 'SO*,CA001')")
    p.add_argument("--skip", default="", help="skip these rule ids/patterns, comma-separated")
    p.add_argument("--include-examples", action="store_true", help="treat _Examples/ as real records")
    p.add_argument("--no-git", action="store_true", help="do not call git (sign-off checks become unverifiable)")
    p.add_argument("--strict", action="store_true", help="warnings count as errors for the exit code")
    p.add_argument("--edition", choices=["standard", "lite"], help="override the edition declared in the schema")
    p.add_argument("--changed-since", metavar="REF", help="only report files changed since a git ref")
    return p.parse_args(argv)


def changed_files(git: Git, ref: str, vault_root: Path) -> set[str] | None:
    if not git.available:
        return None
    try:
        out = subprocess.run(["git", "-c", "core.quotepath=off", "diff", "--name-only", ref, "--", "."],
                             cwd=str(vault_root), capture_output=True, text=True, encoding="utf-8")
    except OSError:
        return None
    if out.returncode != 0:
        return None
    prefix = vault_root.resolve().relative_to(git.top).as_posix()
    prefix = "" if prefix == "." else prefix + "/"
    return {line[len(prefix):] for line in out.stdout.splitlines() if line.startswith(prefix)}


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.vault).resolve()
    if not root.is_dir():
        print(f"vault not found: {root}", file=sys.stderr)
        return 2
    started = time.perf_counter()
    try:
        schema = load(root)
    except SchemaError as exc:
        print(f"schema error: {exc}", file=sys.stderr)
        return 2
    vault = Vault(root, schema)
    git = None if args.no_git else Git(root)
    ctx = Context(vault=vault, options=args, git=git)
    edition = args.edition or schema.edition
    rules = select(all_rules(edition), [r for r in args.rules.split(",") if r], [r for r in args.skip.split(",") if r])
    findings = []
    for rule_id, fn in rules.items():
        findings.extend(fn(ctx))
    if args.changed_since:
        changed = changed_files(git, args.changed_since, root) if git else None
        if changed is not None:
            findings = [f for f in findings if f.path in changed]
    summary = report.summarise(findings, len(vault.notes), time.perf_counter() - started)
    if args.format == "json":
        print(report.as_json(findings, summary, root.as_posix(), schema.version))
    else:
        print(report.as_text(findings, summary))
    failing = summary["errors"] + (summary["warnings"] if args.strict else 0)
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
