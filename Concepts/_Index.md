---
type: index
id: index-concepts
title: "Concepts"
description: "Index of concept and idea notes."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Concepts

Permanent notes for recurring topics, techniques, genes and pathways.

Create with **New record → concept**. Add synonyms to `search_terms`; each concept note then
lists every daily note that mentions it.

```dataview
TABLE WITHOUT ID file.link AS "Concept", aliases AS "Aliases", updated AS "Updated"
FROM "Concepts"
WHERE file.name != "_Index"
SORT file.name ASC
```
