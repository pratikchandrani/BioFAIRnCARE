<%*
/* TEMPLATE-INFO
template_id: TPL-DAILY
name: Daily note
category: Daily
version: 2.1.0
status: active
lab_owned: true
original_author: Pratik Chandrani
original_date: 2026-08-23
source_release: Lab Vault 2.0.0
base_template_id:
base_version:
customised_by:
customised_on:
customisation_summary:
CHANGELOG
| version | date       | author           | summary |
|---------|------------|------------------|---------|
| 1.0.0   | 2026-08-23 | Pratik Chandrani | Lab Vault 1.x daily template: title, open tasks, daily work updates, notes of the past week |
| 2.0.0   | 2026-10-01 | Pratik Chandrani | Adds FAIR properties, FAIR reminder, New experiment / New record / Log buttons, experiments touched today; open tasks via Tasks |
| 2.1.0   | 2026-10-02 | Pratik Chandrani | Add OKF fields title, description and tags |
END TEMPLATE-INFO */
const settingsFile = app.vault.getAbstractFileByPath("Resources/Vault settings.md");
const settings = (settingsFile && app.metadataCache.getFileCache(settingsFile)?.frontmatter) || {};
const today = tp.date.now("YYYY-MM-DD");
-%>
---
type: daily
id: <% tp.file.title %>
title: "<% tp.file.title %>"
description:
tags:
  - daily
created: <% today %>
updated: <% today %>
status: open
owner: <% settings.owner || "" %>
projects: []
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
template_id: TPL-DAILY
template_version: 2.1.0
---
# <% tp.file.title %>

## Tasks due from earlier

```tasks
not done
path does not include Resources/
path does not include _Examples
group by filename
sort by created
```

---

> [!tip] FAIR reminder
> Link what you used — **materials** (with lot numbers), **samples**, the **protocol version** —
> and say **where the raw data lives**. Doing a specific experiment? Click **New experiment**: it
> opens a separate record and adds `- Performed [[…]]` here for you to extend. Small files (≤ 10 MB)
> go in `files/`; large data and code get a **data/code reference** (New record).

```dataviewjs
await dv.view("Resources/lab_resources/scripts/lab-buttons", { buttons: ["new-experiment", "log", "new-record"] });
```

## Daily work updates

%% One block per project or topic you touched today. Start each block with its tag on its own
line, e.g. #Projects/YourProject, then bullet points. Journal club → #JC, Wonder of the Week → #WoW.
Click "New experiment" (or Ctrl+Alt+E) with the cursor inside a block to start a structured record. %%



## End of daily work updates

## Experiments touched today

```dataview
LIST
FROM [[]] AND "Experiments"
SORT file.name ASC
```

## List of notes in past week

```dataview
TABLE file.ctime AS "Created"
WHERE file.ctime >= date(today) - dur(7 days)
  AND !contains(file.path, "Resources/")
  AND !contains(file.path, "_Examples")
SORT file.ctime DESC
```
