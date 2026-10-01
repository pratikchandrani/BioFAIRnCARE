---
type: index
id: index-projects
title: "Projects"
description: "Index of project notes that compile daily-log blocks and linked experiments."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Project index

Every project note and its tag. Check here before creating a new project tag.

Before inventing a new `#Projects/...` tag, check the list below and reuse an existing one.
To start a project: run **New record → project** (creates the project note here), then use its
tag at the start of each related block in your daily notes.

```dataview
TABLE WITHOUT ID file.link AS "Project", project_tag AS "Tag", status AS "Status", pi AS "PI", start_date AS "Started"
FROM "Projects/Auto_summary"
WHERE type = "project" AND !example
SORT status ASC, file.name ASC
```
