---
type: index
id: index-literature
title: "Literature notes"
description: "Index of literature notes imported from Zotero."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Literature notes

Notes imported from Zotero, named by citekey.

Imported with **Zotero Integration** (opt-in plugin, desktop only; see the Obsidian guide) or
written with **New record → literature note**. Name notes by citekey.

```dataview
TABLE WITHOUT ID file.link AS "Citekey", year AS "Year", journal AS "Journal", status AS "Status"
FROM "Zotero_PDF_notes"
WHERE file.name != "_Index"
SORT file.name ASC
```
