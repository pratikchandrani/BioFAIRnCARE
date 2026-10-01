---
type: index
id: index-events
title: "Events"
description: "Index of events: journal clubs, lab meetings, talks and conferences."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Events

Journal clubs (#JC), Wonder of the Week (#WoW), conferences, talks, lab meetings.

Quick entries live in daily notes under `#JC` / `#WoW`; longer write-ups are event notes
(**New record → event**).

```dataview
TABLE WITHOUT ID file.link AS "Event", event_type AS "Type", date AS "Date", presenter AS "Presenter"
FROM "Events"
WHERE file.name != "_Index"
SORT date DESC
```

### Recent #JC and #WoW entries in daily notes

```dataview
LIST
FROM (#JC OR #WoW) AND "daily_notes"
SORT file.name DESC
LIMIT 20
```
