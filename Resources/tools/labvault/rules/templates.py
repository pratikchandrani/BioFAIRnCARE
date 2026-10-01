"""TP rules: TEMPLATE-INFO blocks, catalogue, skeletons, local customisations, note references."""

from __future__ import annotations

from .. import frontmatter as fmlib
from .. import template_info as ti
from ..frontmatter import is_empty
from ..vault import NOTE_TEMPLATES_DIR
from . import finding

LOCAL_DIR = NOTE_TEMPLATES_DIR + "local/"


def _parsed(ctx):
    """Cache: rel -> (TemplateInfo | TemplateInfoError, skeleton Frontmatter | FrontmatterError | None)."""
    cache = getattr(ctx, "_tp_cache", None)
    if cache is not None:
        return cache
    cache = {}
    for t in ctx.vault.templates:
        try:
            info = ti.parse(t.text)
        except ti.TemplateInfoError as exc:
            cache[t.rel] = (exc, None)
            continue
        skeleton = None
        body = ti.body_after(t.text, info)
        if body.lstrip("\n").startswith("---"):
            try:
                skeleton = fmlib.parse(body.lstrip("\n"))
            except fmlib.FrontmatterError as exc:
                skeleton = exc
        cache[t.rel] = (info, skeleton)
    ctx._tp_cache = cache
    return cache


def _infos(ctx):
    return {rel: info for rel, (info, _) in _parsed(ctx).items() if isinstance(info, ti.TemplateInfo)}


def lab_versions(ctx) -> dict:
    """template_id -> lab-owned TemplateInfo."""
    out = {}
    for rel, info in _infos(ctx).items():
        if not rel.startswith(LOCAL_DIR) and not info.is_local:
            out[info.get("template_id")] = info
    return out


def tp001(ctx):
    for rel, (info, skeleton) in _parsed(ctx).items():
        if isinstance(info, ti.TemplateInfoError):
            yield finding("TP001", "error", rel, f"TEMPLATE-INFO missing or malformed: {info}", info.line)
        elif isinstance(skeleton, fmlib.FrontmatterError):
            yield finding("TP001", "error", rel, f"template frontmatter skeleton is not valid: {skeleton}")


def tp002(ctx):
    for rel, info in _infos(ctx).items():
        last = info.changelog[-1]["version"]
        if last != info.get("version"):
            yield finding("TP002", "error", rel, f"CHANGELOG last version {last} != version {info.get('version')}")
        version = info.get("version")
        ok = ti.LOCAL_RE.match(version) if info.is_local else ti.SEMVER_RE.match(version)
        if not ok:
            yield finding("TP002", "error", rel, f"version '{version}' is not valid semver"
                          + (" local label (<base>-local.<n>)" if info.is_local else ""))


def tp003(ctx):
    infos = _infos(ctx)
    files = {t.rel for t in ctx.vault.templates}
    for entry in ctx.schema.catalogue:
        f = entry.get("file")
        if f not in files:
            yield finding("TP003", "error", "Resources/lab_resources/schema/note-types.json",
                          f"catalogue entry {entry.get('code')} points to missing template '{f}'")
            continue
        info = infos.get(f)
        if info and info.get("template_id") != entry.get("template_id"):
            yield finding("TP003", "error", f, f"template_id {info.get('template_id')} != catalogue "
                          f"{entry.get('template_id')} for {entry.get('code')}")


def tp004(ctx):
    schema = ctx.schema
    for rel, (info, skeleton) in _parsed(ctx).items():
        if not isinstance(info, ti.TemplateInfo) or not isinstance(skeleton, fmlib.Frontmatter):
            continue
        ntype = skeleton.data.get("type")
        tdef = schema.type_def(ntype) if isinstance(ntype, str) else None
        if tdef is None:
            yield finding("TP004", "error", rel, f"template skeleton has unknown type {ntype!r}")
            continue
        needed = list(schema.core_required) + tdef.get("required", []) + tdef.get("required_keys", [])
        missing = [k for k in dict.fromkeys(needed) if k not in skeleton.data]
        if missing:
            yield finding("TP004", "error", rel, "template skeleton lacks keys: " + ", ".join(missing))


def tp005(ctx):
    for rel, (info, skeleton) in _parsed(ctx).items():
        if not isinstance(info, ti.TemplateInfo) or not isinstance(skeleton, fmlib.Frontmatter):
            continue
        tid, tver = skeleton.data.get("template_id"), skeleton.data.get("template_version")
        if str(tid) != info.get("template_id") or str(tver) != info.get("version"):
            yield finding("TP005", "error", rel, f"frontmatter template_id/version ({tid} {tver}) != "
                          f"TEMPLATE-INFO ({info.get('template_id')} {info.get('version')})")


def tp006(ctx):
    for rel, info in _infos(ctx).items():
        if not (rel.startswith(LOCAL_DIR) or info.is_local):
            continue
        if not rel.startswith(LOCAL_DIR) or not rel[:-3].endswith("-local"):
            yield finding("TP006", "error", rel, "local templates must live in Resources/note-templates/local/ "
                          "and end with '-local.md'")
        missing = [k for k in ("base_template_id", "base_version", "customised_by", "customised_on",
                               "customisation_summary") if not info.get(k)]
        if missing:
            yield finding("TP006", "error", rel, "local template missing: " + ", ".join(missing))
        m = ti.LOCAL_RE.match(info.get("version", ""))
        if not m or (info.get("base_version") and m.group(1) != info.get("base_version")):
            yield finding("TP006", "error", rel, f"local version '{info.get('version')}' must be "
                          f"'{info.get('base_version') or '<base>'}-local.<n>'")
        if info.get("base_template_id") and info.get("base_template_id") != info.get("template_id"):
            yield finding("TP006", "error", rel, "template_id of a local copy must equal base_template_id")


def tp007(ctx):
    labs = lab_versions(ctx)
    for rel, info in _infos(ctx).items():
        if not info.is_local:
            continue
        lab = labs.get(info.get("base_template_id"))
        base = info.get("base_version")
        if lab and base and ti.version_key(base) < ti.version_key(lab.get("version")):
            yield finding("TP007", "info", rel, f"update available: based on {base}, lab template is now "
                          f"{lab.get('version')}", suggestion="review the lab CHANGELOG and port changes to your copy")


def tp008(ctx):
    known = {}
    for info in _infos(ctx).values():
        versions = known.setdefault(info.get("template_id"), set())
        versions.update(row["version"] for row in info.changelog)
    for note in ctx.typed_notes():
        tid, tver = note.data.get("template_id"), note.data.get("template_version")
        if is_empty(tid):
            continue
        if tid not in known:
            yield finding("TP008", "warning", note, f"unknown template_id '{tid}'", note.line_of("template_id"))
        elif not is_empty(tver) and str(tver) not in known[tid]:
            yield finding("TP008", "warning", note, f"template {tid} has no version '{tver}' in its CHANGELOG",
                          note.line_of("template_version"))


RULES = {"TP001": tp001, "TP002": tp002, "TP003": tp003, "TP004": tp004, "TP005": tp005,
         "TP006": tp006, "TP007": tp007, "TP008": tp008}
