---
type: index
id: index-daily-notes
title: "Daily notes"
description: "Index of daily notes, the primary record of each working day."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Daily notes

One note per day, named YYYY-MM-DD. Open today's note with the ribbon calendar icon or the command *Daily notes: Open today's daily note*.

```dataview
TABLE WITHOUT ID file.link AS "Day", length(file.outlinks) AS "Links", projects AS "Projects"
FROM "daily_notes"
WHERE file.name != "_Index"
SORT file.name DESC
LIMIT 60
```

Older days: use the calendar on [[Home]] or search `path:daily_notes`.
