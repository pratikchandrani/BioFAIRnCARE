---
type: index
id: index-todo
title: "Todo lists"
description: "Index of to-do lists and open tasks."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Todo lists

Kanban boards and long-running checklists.

Any line `- [ ] …` anywhere in the vault is a task. Long-running checklists and Kanban boards
(create one with the command *Kanban: Create new board*) live in this folder.

## Boards and lists

```dataview
LIST
FROM "Todo Lists"
WHERE file.name != "_Index"
```

## All open tasks

```tasks
not done
path does not include Resources/
path does not include _Examples
group by filename
```
