---
type: index
id: template-register
title: "Template register"
description: "Every note template with its version, origin and change history."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

# Template register

Every template in the vault with its version, origin and change history. Each template file
starts with a **TEMPLATE-INFO** block (inside a Templater comment, so it never appears in your
notes) holding its ID, version, original author/date, source release, any local customisation,
and a CHANGELOG. Every note you create records `template_id` and `template_version`, so you can
always tell which version of a template a note came from.

## All templates

```dataviewjs
const files = app.vault.getMarkdownFiles().filter(f => f.path.startsWith("Resources/templates/") || f.path.startsWith("Resources/note-templates/")).sort((a, b) => a.path.localeCompare(b.path));
const parse = (text) => {
  const block = (text.split("/* TEMPLATE-INFO")[1] || "").split("END TEMPLATE-INFO")[0];
  const [head, log = ""] = block.split("CHANGELOG");
  const o = {};
  for (const line of head.split("\n")) { const i = line.indexOf(":"); if (i > 0) o[line.slice(0, i).trim()] = line.slice(i + 1).trim(); }
  const rows = log.split("\n").filter(l => l.trim().startsWith("|")).slice(2).map(l => l.split("|").map(c => c.trim()).filter((c, i, a) => i > 0 && i < a.length - 1));
  o.last = rows.length ? rows[rows.length - 1][1] : "";
  return o;
};
const key = (v) => { const m = String(v || "").match(/^(\d+)\.(\d+)\.(\d+)(?:-local\.(\d+))?$/); return m ? m.slice(1).map(x => parseInt(x || "0", 10)) : [0, 0, 0, 0]; };
const older = (a, b) => { const x = key(a), y = key(b); for (let i = 0; i < 3; i++) { if (x[i] !== y[i]) return x[i] < y[i]; } return false; };
const infos = [];
for (const f of files) infos.push({ f, i: parse(await app.vault.cachedRead(f)) });
const lab = {};
for (const { i } of infos) if (i.lab_owned === "true") lab[i.template_id] = i.version;
const rows = infos.filter(({ i }) => i.template_id).map(({ f, i }) => {
  const local = i.lab_owned === "false";
  const update = local && lab[i.base_template_id] && older(i.base_version, lab[i.base_template_id]) ? `⚠️ update available (lab ${lab[i.base_template_id]})` : "";
  return [dv.fileLink(f.path, false, f.basename), i.template_id, i.category, i.version, i.status, i.last, local ? `local (from ${i.base_version}) — ${i.customisation_summary}` : "lab", update];
});
dv.table(["Template", "ID", "Category", "Version", "Status", "Last change", "Owner", "Update"], rows);
```

## How to customise a template

1. Run **Customise template** (`Ctrl/Cmd+Alt+T`), pick the lab template, write one line saying what
   you will change.
2. Your copy appears in `Resources/note-templates/local/<name>-local.md` with version
   `<lab version>-local.1`, your name, the date and your summary recorded in its TEMPLATE-INFO.
   Edit it freely.
3. *New experiment* / *New record* now offer your copy instead of the lab one, and notes created
   from it record `template_version: <lab version>-local.N`.
4. Each time you change your copy again, bump `version` to `-local.2`, `-local.3`, … and add a row
   to its CHANGELOG.
5. When the lab releases a newer version of the original, the **Update** column above shows
   ⚠️ — read the lab template's CHANGELOG and copy over what you need.

Never edit the lab templates themselves (in `experiments/`, `records/`, `commands/`, `daily.md`):
every lab update replaces them, and your edits would be lost (Git history can still recover
them).

## Versioning rules (lab templates)

| Change | Version bump | Example |
|--------|--------------|---------|
| Removes or renames a property or section | MAJOR (2.0.0) | `lot` renamed to `lot_no` |
| Adds a property, section or parameter row | MINOR (1.1.0) | new *transfer buffer* parameter in C2 |
| Wording, help text, typo | PATCH (1.0.1) | clearer instructions |

Every bump adds a CHANGELOG row (version, date, author, summary). Notes created from older
versions stay valid against the version they declare.

## Retiring a template

Set `status: retired` in its TEMPLATE-INFO (the file stays where it is so old notes keep their
reference). Retired templates are hidden from *New experiment* and *New record*.
