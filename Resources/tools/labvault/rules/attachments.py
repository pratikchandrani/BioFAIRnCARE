"""AT rules: in-vault attachments are small, open-format, named by ID and kept in files/."""

from __future__ import annotations

from ..vault import EXAMPLES_DIR, LAB_RESOURCES_DIR
from . import finding

ATTACH_DIRS = ("files/", EXAMPLES_DIR + "files/")


def _ext(rel: str) -> str:
    name = rel.rsplit("/", 1)[-1].lower()
    return name.rsplit(".", 1)[-1] if "." in name else ""


def at001(ctx):
    limit = ctx.vault.max_attachment_bytes()
    for rel in ctx.vault.attachments:
        size = (ctx.vault.root / rel).stat().st_size
        if size > limit:
            yield finding("AT001", "error", rel,
                          f"attachment is {size / 1048576:.1f} MB (limit {limit / 1048576:.0f} MB)",
                          suggestion="move it to lab storage and register it with New record → data reference")


def at002(ctx):
    raw = ctx.schema.raw_ext
    for rel in ctx.vault.attachments:
        name = rel.lower()
        ext = _ext(rel)
        if ext in raw or name.endswith((".fastq.gz", ".fq.gz", ".vcf.gz")):
            yield finding("AT002", "error", rel, f"raw/proprietary format '.{ext}' must not be stored in the vault",
                          suggestion="keep it in lab storage and register a DATA- reference note")


def at003(ctx):
    pattern = ctx.schema.attachment_name
    for rel in ctx.vault.attachments:
        if not rel.startswith(ATTACH_DIRS):
            continue
        name = rel.rsplit("/", 1)[-1]
        if not pattern.match(name):
            yield finding("AT003", "warning", rel, "attachment not named <ID>_<short-description>_<YYYYMMDD>.<ext>",
                          suggestion="rename in Obsidian (links update automatically), e.g. "
                                     "EXP-AB-20261001-01_gel_20261001.png")


def at004(ctx):
    v = ctx.vault
    referenced = set()
    for note in v.notes:
        for link in note.links:
            target = v.resolve(link.target, note.rel)
            if target:
                referenced.add(target)
    for rel in v.attachments:
        if rel.startswith(LAB_RESOURCES_DIR):
            continue
        if not rel.startswith(ATTACH_DIRS):
            yield finding("AT004", "warning", rel, "attachment outside files/",
                          suggestion="move it into files/ (Obsidian updates links)")
        elif rel not in referenced:
            yield finding("AT004", "warning", rel, "attachment is not linked from any note")


RULES = {"AT001": at001, "AT002": at002, "AT003": at003, "AT004": at004}
