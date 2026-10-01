---
type: index
id: vault-health
title: "Vault Health"
description: "Live check of your vault inside Obsidian, with the fix for every problem it finds."
created: 2026-10-01
updated: 2026-10-02
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Vault Health

A live check of your vault that runs inside Obsidian (desktop and mobile, no Python needed). It is
a **subset** of the full validator `Resources/tools/validate_vault.py`, which runs every rule.
Rule codes match the validator so you can look them up in the guides.
The validator additionally checks Git history (sign-off by a reviewer, edits after sign-off).

Re-open this note (or switch away and back) to refresh. Examples in `_Examples/` are checked
separately and never count against your own records.

```dataviewjs
const SCHEMA = "Resources/lab_resources/schema/note-types.json";
const schema = JSON.parse(await app.vault.adapter.read(SCHEMA));
const fmOf = (f) => app.metadataCache.getFileCache(f)?.frontmatter;
const empty = (v) => v === undefined || v === null || v === "" || (Array.isArray(v) && v.length === 0);
const skip = (p) => p.startsWith("Resources/templates/") || p.startsWith("Resources/note-templates/") || p.startsWith("Resources/tools/");
const findings = [];
const add = (rule, sev, path, msg) => findings.push({ rule, sev, path, msg });
const matches = (when, d) => Object.entries(when || {}).every(([k, allowed]) => allowed.includes(d[k]));

const notes = app.vault.getMarkdownFiles().filter(f => !skip(f.path));
const ids = {};
for (const f of notes) {
  const d = fmOf(f);
  const isEx = f.path.startsWith("_Examples/");
  if (!d || !d.type) continue;
  const tdef = schema.types[d.type];
  if (!tdef) { add("FM004", "error", f.path, `unknown type '${d.type}'`); continue; }
  const miss = schema.core_required.filter(k => empty(d[k]));
  if (miss.length) add("FM002", "error", f.path, "missing core properties: " + miss.join(", "));
  const req = (tdef.required || []).filter(k => empty(d[k]));
  const keys = (tdef.required_keys || []).filter(k => !(k in d));
  if (req.length) add("FM003", "error", f.path, "missing: " + req.join(", "));
  if (keys.length) add("FM003", "error", f.path, "missing property keys: " + keys.join(", "));
  if (!empty(d.status) && !tdef.status.includes(d.status)) add("FM004", "error", f.path, `status '${d.status}' not allowed`);
  for (const c of [...(schema.common_conditional || []), ...(tdef.conditional || [])]) {
    if (!matches(c.when, d)) continue;
    const m = [...(c.require || []), ...((schema.groups[c.require_group] || []))].filter(k => empty(d[k]));
    if (c.require_any && c.require_any.every(k => empty(d[k]))) m.push(c.require_any.join(" or "));
    for (const [k, v] of Object.entries(c.equals || {})) if (d[k] !== v) m.push(`${k} must be ${v}`);
    if (m.length) add(c.rule || "FM003", c.rule === "CA002" ? "warning" : "error", f.path, "missing / wrong: " + [...new Set(m)].join(", "));
  }
  if (!empty(d.id)) {
    const key = (isEx ? "ex:" : "") + d.id;
    (ids[key] = ids[key] || []).push(f.path);
  }
  if (isEx && d.example !== true) add("EX001", "error", f.path, "note in _Examples/ needs example: true");
  if (!isEx && d.example === true) add("EX001", "error", f.path, "example: true outside _Examples/");
}
// LK004: every experiment must be linked from or to a daily note
const dailyPaths = new Set(notes.filter(f => fmOf(f)?.type === "daily").map(f => f.path));
const traced = new Set();
for (const [src, targets] of Object.entries(app.metadataCache.resolvedLinks)) {
  for (const t of Object.keys(targets)) {
    if (dailyPaths.has(src)) traced.add(t);
    if (dailyPaths.has(t)) traced.add(src);
  }
}
for (const f of notes) {
  if (fmOf(f)?.type === "experiment" && !traced.has(f.path)) add("LK004", "warning", f.path, "experiment not linked from or to any daily note — add '- Performed [[…]]' to that day's note");
}
// OK001–OK004: Open Knowledge Format (OKF v0.2) — see the OKF guide
const okfCfg = schema.okf || {};
const okfExempt = (p) => (okfCfg.exempt_prefixes || []).some(x => p.startsWith(x));
const reserved = new Set((okfCfg.reserved_names || ["index.md", "log.md"]).map(s => s.toLowerCase()));
const finished = new Set(okfCfg.finished_experiment_statuses || ["completed"]);
const descMax = okfCfg.description_max || 200;
for (const f of app.vault.getMarkdownFiles()) {
  if (reserved.has(f.name.toLowerCase())) add("OK002", "error", f.path, "file name reserved by OKF (index.md / log.md) — rename it");
  if (okfExempt(f.path)) continue;
  const d = fmOf(f);
  if (!d) { add("OK001", "error", f.path, "no properties: OKF needs a 'type' — create the note from its template"); continue; }
  if (empty(d.type)) { add("OK001", "error", f.path, "'type' is empty"); continue; }
  if (empty(d.title)) add("OK003", "info", f.path, "add a 'title'");
  if (d.type !== "daily" && empty(d.description)) add("OK003", "info", f.path, "add a one-sentence 'description'");
  else if (typeof d.description === "string" && d.description.length > descMax) add("OK003", "info", f.path, `shorten 'description' to one sentence (≤ ${descMax} characters)`);
  if (d.type === "experiment" && finished.has(d.status) && empty(d.description)) add("OK004", "warning", f.path, `${d.status} experiment without a 'description' — describe what was done and found`);
}
for (const [id, paths] of Object.entries(ids)) if (paths.length > 1) for (const p of paths) add("ID002", "error", p, `duplicate id ${id.replace(/^ex:/, "")}`);

const resolved = app.metadataCache.resolvedLinks;
for (const [src, targets] of Object.entries(app.metadataCache.unresolvedLinks)) {
  if (skip(src)) continue;
  for (const t of Object.keys(targets)) add("LK001", "error", src, `unresolved link [[${t}]]`);
}
for (const [src, targets] of Object.entries(resolved)) {
  if (skip(src) || src.startsWith("_Examples/")) continue;
  for (const t of Object.keys(targets)) if (t.startsWith("_Examples/")) add("EX002", "error", src, `links into _Examples/ (${t})`);
}

const settingsFile = app.vault.getAbstractFileByPath("Resources/Vault settings.md");
const limitMb = Number((settingsFile && fmOf(settingsFile)?.max_attachment_mb) || schema.max_attachment_mb || 10);
const namePat = new RegExp(schema.attachment_name_pattern);
for (const f of app.vault.getFiles()) {
  const p = f.path, ext = (f.extension || "").toLowerCase();
  if (["md", "base", "canvas"].includes(ext) || p.startsWith(".") || skip(p) || p.startsWith("Resources/lab_resources/")) continue;
  if (["gitkeep", "gitignore"].includes(ext) || ["LICENSE", "VERSION"].includes(f.name)) continue;
  if (f.stat.size > limitMb * 1048576) add("AT001", "error", p, `${(f.stat.size / 1048576).toFixed(1)} MB > ${limitMb} MB — register it as a data reference`);
  if (schema.raw_extensions_disallowed.includes(ext)) add("AT002", "error", p, `raw format .${ext} must stay outside the vault`);
  const inFiles = p.startsWith("files/") || p.startsWith("_Examples/files/");
  if (inFiles && !namePat.test(f.name)) add("AT003", "warning", p, "rename to <ID>_<description>_<YYYYMMDD>.<ext>");
  if (!inFiles) add("AT004", "warning", p, "attachment outside files/");
}

const reg = app.vault.getAbstractFileByPath("Resources/lab_resources/Plugin register.md");
if (reg) {
  const text = await app.vault.cachedRead(reg);
  const section = text.split("## Registered plugins")[1]?.split("\n## ")[0] || "";
  const rows = section.split("\n").filter(l => l.trim().startsWith("|")).slice(2).map(l => l.split("|").map(c => c.trim()));
  const regEnabled = new Set(rows.filter(r => r[4] === "enabled").map(r => r[1]));
  const enabled = new Set([...(app.plugins?.enabledPlugins || [])]);
  for (const id of enabled) if (!regEnabled.has(id) && !rows.some(r => r[1] === id && r[4] === "opt-in")) add("PL001", "error", "community plugins", `plugin '${id}' is enabled but not registered`);
  for (const id of regEnabled) if (!enabled.has(id)) add("PL001", "warning", "community plugins", `registered plugin '${id}' is not enabled`);
}

const own = findings.filter(x => !x.path.startsWith("_Examples/") && x.sev !== "info");
const tips = findings.filter(x => !x.path.startsWith("_Examples/") && x.sev === "info");
const ex = findings.filter(x => x.path.startsWith("_Examples/"));
const count = (arr, s) => arr.filter(x => x.sev === s).length;
dv.paragraph(`**Your records:** ${count(own, "error")} errors, ${count(own, "warning")} warnings, ${tips.length} suggestions · **Examples:** ${count(ex, "error")} errors`);
const show = (arr) => arr.length
  ? dv.table(["Rule", "Severity", "Where", "What"], arr.sort((a, b) => a.sev.localeCompare(b.sev) || a.path.localeCompare(b.path)).map(x => [x.rule, x.sev, x.path.endsWith(".md") ? dv.fileLink(x.path) : x.path, x.msg]))
  : dv.paragraph("✅ Nothing to fix.");
show(own);
if (tips.length) {
  dv.header(3, "Suggestions (OKF properties — never block anything)");
  dv.table(["Rule", "Where", "What"], tips.sort((a, b) => a.path.localeCompare(b.path)).map(x => [x.rule, dv.fileLink(x.path), x.msg]));
}
if (ex.length) { dv.header(3, "Examples"); show(ex); }
```

## What the rule codes mean

| Code | Meaning | Fix |
|------|---------|-----|
| FM002 / FM003 | Required property missing | Fill it in the Properties panel |
| FM004 | Value not allowed (type, status, enum) | Use one of the allowed values |
| ID002 | Two notes share an ID | Renumber the newer note nobody links to yet |
| LK001 | Link to a note that does not exist | Fix the spelling or create the note |
| LK004 | Experiment not linked from any daily note | Add `- Performed [[<experiment>]]` to the daily note of that day |
| AT001 / AT002 | File too big or raw format in the vault | Move it to lab storage; create a data reference |
| AT003 / AT004 | Attachment badly named or outside `files/` | Rename / move it (links update automatically) |
| CA001 / CA002 | CARE fields missing for human/community data | See the [[CARE guide]] |
| AN001 | Animal-ethics fields missing | IAEC approval, humane end-points, 3Rs |
| BS001 | Biosafety level / IBSC approval missing | Fill `biosafety_level` (and `ibsc_approval` for BSL-2+) |
| DR001 / DR002 | Data / code reference incomplete | Location, format, size, checksum, steward, access / repository, commit or tag, entry point |
| EX001 / EX002 | Example content mixed with real notes | Keep examples in `_Examples/`; do not link to them |
| PL001 | Plugin list differs from the [[Plugin register]] | Ask the maintainer before adding plugins |
| OK001 | Note without properties or with an empty `type` (OKF) | Create the note from its template, or add properties with a `type` |
| OK002 | File named `index.md` or `log.md` (reserved by OKF) | Rename it |
| OK003 | Suggestion: no `title` / `description`, or description too long | Add a one-sentence description ([[OKF guide]]) |
| OK004 | Finished experiment without a `description` | Describe what was done and found in one sentence |

| Code | Meaning | Fix |
|------|---------|-----|
| SO001 | Signed-off note without reviewer and date | Only the reviewer signs off (see the student guide) |
