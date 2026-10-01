<%*
/* TEMPLATE-INFO
template_id: TPL-R-CONCEPT
name: Concept
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
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Initial template |
| 1.1.0   | 2026-10-02 | Pratik Chandrani | Add OKF fields title, description and tags |
END TEMPLATE-INFO */
const settingsFile = app.vault.getAbstractFileByPath("Resources/Vault settings.md");
const settings = (settingsFile && app.metadataCache.getFileCache(settingsFile)?.frontmatter) || {};
const ctx = window.labvaultContext || {};
const today = tp.date.now("YYYY-MM-DD");
const m = tp.file.title.match(/^((?:PRT|SMP|MAT|INS|DATA|CODE|EVT)-[A-Z]{2,4}-\d{8}-\d{2})\s*(.*)$/);
const id = m ? m[1] : tp.file.title;
const title = (m ? m[2] : tp.file.title).replace(/"/g, "'");
const yamlList = (items) => (items && items.length) ? "\n" + items.map(l => '  - "' + l + '"').join("\n") : "[]";
const projects = yamlList((ctx.projects || []).map(p => String(p).startsWith("[[") ? p : "[[" + p + "]]"));
const supersedes = ctx.supersedes ? '"[[' + ctx.supersedes + ']]"' : "";
-%>
---
type: concept
id: <% id %>
title: "<% title %>"
description:
tags:
  - concept
created: <% today %>
updated: <% today %>
status: active
owner: <% settings.owner || "" %>
aliases: []
search_terms: []
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
template_id: TPL-R-CONCEPT
template_version: 1.1.0
---
# <% title %>
Date updated: <% today %>

One-paragraph short definition / summary.

---

## Sub-concepts

### Sub-topic A
-

## Related concepts
- [[ ]] — why it is related

## Resources / references
-

---

## Daily notes discussing this concept

%% Add synonyms and keywords to the `search_terms` property; every daily note that mentions one of
them (or links this note) is listed below automatically. %%

```dataviewjs
const me = dv.current();
const terms = [me.file.name, ...(me.aliases || []), ...(me.search_terms || [])].filter(Boolean).map(t => String(t).toLowerCase());
const folder = me.file.path.startsWith("_Examples/") ? '"_Examples/daily_notes"' : '"daily_notes"';
const rows = [];
for (const p of dv.pages(folder).sort(p => p.file.name, "desc")) {
  const text = (await dv.io.load(p.file.path)).toLowerCase();
  if (terms.some(t => text.includes(t))) rows.push([p.file.link, p.file.name]);
}
rows.length ? dv.table(["Daily note", "Date"], rows) : dv.paragraph("Not mentioned in any daily note yet.");
```
