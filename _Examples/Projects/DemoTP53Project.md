---
type: project
id: DemoTP53Project
title: "DemoTP53Project"
description: "Fictional training project testing whether TP53 knockdown changes cisplatin sensitivity."
tags:
  - project
created: 2026-01-10
updated: 2026-01-15
status: active
owner: Example Student
project_tag: Projects/DemoTP53Project
members:
  - Example Student
pi: Pratik Chandrani
start_date: 2026-01-10
ethics_approval: IEC/EX/2026/001 (fictional)
ibsc_approval: IBSC/EX/2026/004 (fictional)
iaec_approval: IAEC/EX/2026/007 (fictional)
human_or_community_data: false
confidentiality: internal
license: lab-internal
ai_assisted: false
example: true
template_id: TPL-R-PROJECT
template_version: 1.0.0
---
# DemoTP53Project

> [!example] Fictional example project
> Shows how a project note compiles itself from daily-note blocks tagged
> `#Projects/DemoTP53Project` and lists experiments that link to it.

## Aim and background

Test whether TP53 knockdown changes cisplatin sensitivity in a fictional lung adenocarcinoma
cell line (fictional study used only for training).

## Approvals

- Ethics committee (IEC/IRB): `ethics_approval`
- Biosafety (IBSC): `ibsc_approval`
- Animal ethics (IAEC): `iaec_approval`

## Daily log (auto-compiled)

```dataviewjs
const me = dv.current();
const tag = "#" + String(me.project_tag || "").replace(/^#/, "");
const esc = tag.replace(/[.*+?^${}()|[\]\\/]/g, "\$&");
const tagRe = new RegExp("(^|\s)" + esc + "(?=$|[\s:,.;-])");
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
