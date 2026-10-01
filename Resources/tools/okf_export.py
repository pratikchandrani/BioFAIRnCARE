#!/usr/bin/env python3
"""Export a BioFAIRnCARE vault as an Open Knowledge Format (OKF v0.2) bundle — for the PI / maintainer.

Usage:  python Resources/tools/okf_export.py VAULT OUT [--internal] [--examples] [--force]
                                             [--edition standard|lite] [--json]

The vault is never modified. Confidential and embargoed notes are always left out, internal notes
unless --internal, and human-subject / community-data notes unless the PI set
`okf_export: allowed` (constitution v2.3.0, Principle VII; see the OKF guide). The list of left-out
notes is written NEXT TO the bundle (OUT-exclusions.md), never inside it.
Python 3.10+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from labvault import okf  # noqa: E402
from labvault.frontmatter import is_empty  # noqa: E402
from labvault.schema import SchemaError, load  # noqa: E402
from labvault.vault import EXAMPLES_DIR, Vault  # noqa: E402

URI_RE = re.compile(r"^(https?://|doi:|s3://|gs://|file://|ftp://)", re.I)
INLINE_TAG_RE = re.compile(r"(?<![\w/#&])#([A-Za-z][\w/-]*)")
CHANGELOG_RE = re.compile(r"^## \[?([^\]\s]+)\]?\s*-\s*(\d{4}-\d{2}-\d{2})\s*$", re.M)
SKIPPED_KEYS = {"status"}  # replaced by the OKF status + lab_status


def parse_args(argv):
    p = argparse.ArgumentParser(description="Export a BioFAIRnCARE vault as an OKF v0.2 bundle (vault is not changed).")
    p.add_argument("vault", help="vault folder")
    p.add_argument("out", help="output folder (outside the vault; empty or new unless --force)")
    p.add_argument("--internal", action="store_true", help="include 'internal' notes (export stays within the lab)")
    p.add_argument("--examples", action="store_true", help="include the fictional _Examples/ notes")
    p.add_argument("--force", action="store_true", help="clear a non-empty output folder first")
    p.add_argument("--edition", choices=["standard", "lite"], help="default: the schema's edition")
    p.add_argument("--json", action="store_true", help="print the summary as JSON")
    return p.parse_args(argv)


def decide(note, args) -> str | None:
    """Exclusion reason code (data-model §3) or None when the note is exported."""
    d = note.data
    if note.fm_error is not None or not note.fm.present or is_empty(note.type):
        return "not-conformant"
    if note.type == "settings":
        return "not-knowledge"
    if note.path.name.lower() in ("index.md", "log.md"):
        return "reserved-name"
    if note.is_example and not args.examples:
        return "example"
    conf = d.get("confidentiality")
    if conf in ("confidential", "embargoed"):
        return f"confidentiality:{conf}"
    if conf == "internal" and not args.internal:
        return "confidentiality:internal"
    if d.get("human_or_community_data") is True and d.get("okf_export") != "allowed":
        return "care:no-export-permission"
    return None


def at(value) -> str | None:
    return f"{value}T00:00:00Z" if isinstance(value, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", value) else None


def concept_frontmatter(note, vault, conv, edition) -> dict:
    d = note.data
    out = {"type": note.type, "title": d.get("title") or note.stem}
    if not is_empty(d.get("description")):
        out["description"] = d["description"]
    tags = [str(t).lstrip("#") for t in (d.get("tags") or []) if not is_empty(t)] if isinstance(d.get("tags"), list) \
        else ([str(d["tags"]).lstrip("#")] if not is_empty(d.get("tags")) else [])
    for m in INLINE_TAG_RE.finditer(okf.strip_comments(note.fm.body)):
        if m.group(1) not in tags:
            tags.append(m.group(1))
    if tags:
        out["tags"] = tags
    out["status"] = okf.okf_status(vault.schema, note.type, d.get("status"))
    if not is_empty(d.get("status")):
        out["lab_status"] = d["status"]
    for key in ("location", "repository"):
        if isinstance(d.get(key), str) and URI_RE.match(d[key]):
            out["resource"] = d[key]
            break
    generated = {"by": okf.actor(vault, d.get("owner"), d.get("id"))}
    when = at(d.get("updated")) or at(d.get("created"))
    if when:
        generated["at"] = when
    if d.get("ai_assisted") is True:
        generated["assisted_by"] = d.get("ai_note") or "AI tool (see the note)"
    out["generated"] = generated
    if edition == "standard" and not is_empty(d.get("signed_off_by")) and at(d.get("signed_off_on")):
        out["verified"] = [{"by": okf.actor(vault, d["signed_off_by"]), "at": at(d["signed_off_on"])}]
    for key, value in d.items():
        if key in out or key in SKIPPED_KEYS or key in ("tags",):
            continue
        out[key] = conv.value(value, note.rel)
    return out


def plural(n: int) -> str:
    return f"{n} note" if n == 1 else f"{n} notes"


def folder_title(rel_dir: str) -> str:
    return rel_dir.rsplit("/", 1)[-1] if rel_dir else "BioFAIRnCARE knowledge bundle"


def write_indexes(out: Path, exported: dict[str, dict]) -> None:
    """index.md per folder (no frontmatter) and the bundle root (okf_version only), OKF §8."""
    folders: dict[str, list[str]] = {}
    for rel in exported:
        parts = rel.split("/")
        for i in range(len(parts)):
            folders.setdefault("/".join(parts[:i]), [])
        folders["/".join(parts[:-1])].append(rel)
    for folder in sorted(folders):
        subdirs = sorted(f for f in folders if f and (f.rsplit("/", 1)[0] if "/" in f else "") == folder)
        lines = [f"# {folder_title(folder)}", ""]
        if folder == "":
            lines += ["OKF v0.2 bundle exported from a BioFAIRnCARE vault. Links are bundle-relative; see EXPORT-REPORT.md.", ""]
        if subdirs:
            lines += ["## Folders", ""]
            lines += [f"* [{folder_title(s)}]({okf.bundle_link(s + '/index.md')}) - "
                      f"{plural(len([r for r in exported if r.startswith(s + '/')]))}" for s in subdirs]
            lines.append("")
        notes = sorted(folders[folder], key=lambda r: str(exported[r].get("title", r)).lower())
        if notes:
            lines += ["## Notes", ""]
            for rel in notes:
                fm = exported[rel]
                desc = f" - {fm['description']}" if fm.get("description") else ""
                lines.append(f"* [{fm.get('title', rel)}]({okf.bundle_link(rel)}){desc}")
            lines.append("")
        head = f'---\nokf_version: "{okf.OKF_VERSION}"\n---\n' if folder == "" else ""
        target = out / folder / "index.md" if folder else out / "index.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(head + "\n".join(lines), encoding="utf-8", newline="\n")


def write_log(out: Path, vault_root: Path, count: int) -> None:
    """log.md (OKF §9): date headings newest first, from the CHANGELOG plus this export."""
    entries: dict[str, list[str]] = {}
    changelog = vault_root / "CHANGELOG.md"
    if changelog.is_file():
        for m in CHANGELOG_RE.finditer(changelog.read_text(encoding="utf-8")):
            entries.setdefault(m.group(2), []).append(f"**Update** BioFAIRnCARE {m.group(1)} released.")
    entries.setdefault(date.today().isoformat(), []).insert(0, f"**Creation** OKF bundle exported ({count} notes).")
    lines = ["# Log", ""]
    for day in sorted(entries, reverse=True):
        lines += [f"## {day}", "", *entries[day], ""]
    (out / "log.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run(args) -> int:
    started = time.perf_counter()
    vault_root = Path(args.vault).resolve()
    out = Path(args.out).resolve()
    if out == vault_root or vault_root in out.parents:
        print("error: the output folder must be outside the vault", file=sys.stderr)
        return 2
    if out.exists() and any(out.iterdir()):
        if not args.force:
            print(f"error: {out} is not empty (use --force to replace it)", file=sys.stderr)
            return 2
        shutil.rmtree(out)
    try:
        schema = load(vault_root)
    except SchemaError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    vault = Vault(vault_root, schema)
    edition = args.edition or schema.edition

    included, excluded = {}, []
    for note in vault.notes:
        if okf.is_exempt(schema, note.rel):
            continue
        reason = decide(note, args)
        if reason:
            excluded.append((note.rel, reason))
        else:
            included[note.rel] = note.rel
    copied = set()
    for rel in included:
        for link in vault.by_rel[rel].links:
            target = vault.resolve(link.target, rel)
            if target in vault.attachments and target.startswith(("files/", EXAMPLES_DIR + "files/")):
                copied.add(target)
    conv = okf.LinkConverter(vault, included, copied)

    out.mkdir(parents=True, exist_ok=True)
    exported = {}
    for rel in sorted(included):
        note = vault.by_rel[rel]
        fm = concept_frontmatter(note, vault, conv, edition)
        body = okf.replace_dynamic_blocks(okf.strip_comments(note.fm.body))
        body = conv.body(body, rel)
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(okf.dump_yaml(fm) + body.lstrip("\n"), encoding="utf-8", newline="\n")
        exported[rel] = fm
    for rel in sorted(copied):
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(vault_root / rel, out / rel)

    reasons = Counter(reason for _, reason in excluded)
    report_fm = {"type": "guide", "title": "Export report",
                 "description": f"How this OKF bundle was produced from a BioFAIRnCARE vault ({len(exported)} notes)."}
    report_lines = ["# Export report", "", f"- Exported notes: {len(exported)}", f"- Attachments: {len(copied)}",
                    f"- Left out: {len(excluded)} (names are listed only outside the bundle)", "",
                    "| Reason | Notes |", "|--------|-------|"]
    report_lines += [f"| {r} | {n} |" for r, n in sorted(reasons.items())]
    report_lines += ["", f"Options: internal={args.internal}, examples={args.examples}, edition={edition}.", ""]
    (out / "EXPORT-REPORT.md").write_text(okf.dump_yaml(report_fm) + "\n".join(report_lines), encoding="utf-8",
                                          newline="\n")
    exported["EXPORT-REPORT.md"] = report_fm
    write_indexes(out, exported)
    write_log(out, vault_root, len(exported) - 1)

    sidecar = out.parent / f"{out.name}-exclusions.md"
    sidecar.write_text("# Notes left out of the OKF export\n\n| Note | Reason |\n|------|--------|\n"
                       + "".join(f"| {rel} | {reason} |\n" for rel, reason in sorted(excluded)),
                       encoding="utf-8", newline="\n")

    problems = okf.check_bundle(out)
    summary = {"exported": len(exported) - 1, "excluded": len(excluded), "reasons": dict(reasons),
               "attachments": len(copied), "conformant": not problems, "problems": problems,
               "exclusions_file": str(sidecar), "seconds": round(time.perf_counter() - started, 2)}
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        why = ", ".join(f"{r}: {n}" for r, n in sorted(reasons.items())) or "none"
        print(f"exported {summary['exported']} notes, excluded {len(excluded)} ({why}), attachments {len(copied)}; "
              f"OKF v{okf.OKF_VERSION} conformance: {'OK' if not problems else 'FAILED'}")
        print(f"left-out notes listed in {sidecar}")
        for p in problems:
            print(f"   {p}")
    return 1 if problems else 0


def main(argv=None) -> int:
    return run(parse_args(argv if argv is not None else sys.argv[1:]))


if __name__ == "__main__":
    sys.exit(main())
