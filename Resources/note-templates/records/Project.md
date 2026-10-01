<%*
/* TEMPLATE-INFO
template_id: TPL-R-PROJECT
name: Project
category: Records
version: 1.1.0
status: active
lab_owned: true
original_author: Pratik Chandrani
original_date: 2026-10-01
source_release: Lab Vault 2.0.0
base_template_id:
base_version:
customised_by:
customised_on:
customisation_summary:
CHANGELOG
| version | date       | author           | summary |
|---------|------------|------------------|---------|
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Project note with auto-compiled daily log (from #Projects/ tag blocks) and linked experiments |
| 1.1.0   | 2026-10-02 | Pratik Chandrani | Add OKF fields title, description and tags |
END TEMPLATE-INFO */
const settingsFile = app.vault.getAbstractFileByPath("Resources/Vault settings.md");
const settings = (settingsFile && app.metadataCache.getFileCache(settingsFile)?.frontmatter) || {};
const today = tp.date.now("YYYY-MM-DD");
-%>
---
type: project
id: <% tp.file.title %>
title: "<% tp.file.title %>"
description:
tags:
  - project
created: <% today %>
updated: <% today %>
status: active
owner: <% settings.owner || "" %>
project_tag: Projects/<% tp.file.title %>
members: []
pi: <% settings.pi || "" %>
start_date: <% today %>
ethics_approval:
ibsc_approval:
iaec_approval:
human_or_community_data: false
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
template_id: TPL-R-PROJECT
template_version: 1.1.0
---
# <% tp.file.title %>

> [!info] How this note fills itself
> Write in your daily notes under a line with the tag `#Projects/<% tp.file.title %>`. Every such
> block appears below automatically, newest first. Experiments whose `projects` property links
> this note are listed at the end. Add this project to the [[Projects/Auto_summary/_Index|Project index]].

## Aim and background

## Approvals

- Ethics committee (IEC/IRB): `ethics_approval`
- Biosafety (IBSC): `ibsc_approval`
- Animal ethics (IAEC): `iaec_approval`

If the project uses human or community-derived material, set `human_or_community_data: true`
and fill the CARE fields (see the CARE guide).

## Daily log (auto-compiled)

```dataviewjs
const me = dv.current();
const tag = "#" + String(me.project_tag || "").replace(/^#/, "");
const esc = tag.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&");
const tagRe = new RegExp("(^|\\s)" + esc + "(?=$|[\\s:,.;-])");
const stopRe = /^(#Projects\/|#JC\b|#WoW\b|---\s*$|#{1,6}\s)/;
const folder = me.file.path.startsWith("_Examples/") ? '"_Examples/daily_notes"' : '"daily_notes"';
const pages = dv.pages(folder).where(p => p.type === "daily" || /^\d{4}-\d{2}-\d{2}$/.test(p.file.name))
  .sort(p => p.file.name, "desc");
let shown = 0;
for (const p of pages) {
  const lines = (await dv.io.load(p.file.path)).split("\n");
  const blocks = [];
  let cur = null;
  for (const ln of lines) {
    const t = ln.trim();
    if (tagRe.test(t)) {
      cur = [];
      blocks.push(cur);
      const rest = t.replace(tagRe, " ").replace(/^[\s:—–-]+/, "").trim();
      if (rest) cur.push("- " + rest);
      continue;
    }
    if (cur && stopRe.test(t)) cur = null;
    if (cur && t) cur.push(ln);
  }
  if (blocks.length) {
    dv.header(4, p.file.link);
    for (const b of blocks) dv.paragraph(b.join("\n"));
    shown++;
  }
}
if (!shown) dv.paragraph("No daily-note blocks tagged " + tag + " yet.");
```

## Linked experiments

```dataview
TABLE id AS "ID", experiment_type AS "Type", status AS "Status", outcome AS "Outcome", start_date AS "Started"
FROM "Experiments" OR "_Examples/Experiments"
WHERE contains(projects, this.file.link) AND (example = this.example)
SORT start_date DESC
```
