---
type: concept
id: Demo apoptosis
title: "Demo apoptosis"
description: "Example concept note on apoptosis and the role of p53 after DNA damage."
tags:
  - concept
  - apoptosis
created: 2026-01-15
updated: 2026-01-15
status: active
owner: Example Student
aliases: []
search_terms:
  - apoptosis
  - cell death
confidentiality: internal
license: lab-internal
ai_assisted: false
example: true
template_id: TPL-R-CONCEPT
template_version: 1.0.0
---
> [!example] Fictional example — all names, numbers and locations are made up.

# Demo apoptosis
Date updated: 2026-01-15

Programmed cell death; p53 promotes apoptosis after DNA damage (e.g. cisplatin).

## Related concepts
- [[DemoTP53Project]] — the demo project tests this link.

## Daily notes discussing this concept

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
