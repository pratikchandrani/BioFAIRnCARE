---
type: index
id: index-tags
title: "Table of Tags"
description: "Overview of the tags used in the vault and what each one means."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Table of Tags

Every tag in the vault and how often it is used.

Rename or merge a tag safely with **Tag Wrangler** (right-click the tag in the Tags pane).

```dataviewjs
const counts = {};
for (const p of dv.pages('-"_Examples" and -"Resources/templates"')) {
  for (const t of (p.file.etags || [])) counts[t] = (counts[t] || 0) + 1;
}
const rows = Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
rows.length ? dv.table(["Tag", "Notes"], rows) : dv.paragraph("No tags yet.");
```
