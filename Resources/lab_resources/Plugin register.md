---
type: index
id: plugin-register
title: "Plugin register"
description: "Every community plugin in the vault with its purpose, version and fallback."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Plugin register

Every community plugin in this vault is listed here (constitution v2.0.0, Principle II). The
validator checks that this table matches the installed plugins and
`.obsidian/community-plugins.json` (rules PL001–PL003).

**Rules for plugins**
- A plugin is added only if no core Obsidian feature does the job, it is open-source and
  maintained, and the maintainer approves it; then it is added to this table.
- Plugins that use the network, a shell, a local server or a native helper program ship
  **opt-in** (installed but switched off). You enable them yourself during setup.
- Your notes never depend on a plugin to be readable: if a plugin is removed, only live views
  (tables, dashboards, buttons) stop working — the *Fallback* column says what to do instead.
- The maintainer reviews this list every quarter and removes plugins that are no longer worth
  their maintenance or security cost.

## Registered plugins

| Plugin id | Name | Version | Default state | Purpose | Vault features that depend on it | Justification | Fallback if removed |
|-----------|------|---------|---------------|---------|----------------------------------|---------------|---------------------|
| dataview | Dataview | 0.5.68 | enabled | Live queries over notes | Home dashboard, project roll-ups, concept back-lists, Table of Tags, Template register, Vault Health, experiment catalogue | Reads note *content* (tagged daily blocks), which core Bases cannot | Core Bases views for property tables; core search for tag blocks |
| templater-obsidian | Templater | 2.25.0 | enabled | Templates with logic | Daily template and the lab commands (New experiment, New record, Log to experiment, Customise template, …), ID generation | One-step creation with IDs and link-back (≤ 3 actions) | Copy a template file by hand and fill the ID manually |
| homepage | Homepage | 4.4.4 | enabled | Open Home on startup | Home dashboard as start page | No core equivalent for open-on-startup | Bookmark Home (core Bookmarks) |
| obsidian-tasks-plugin | Tasks | 8.3.0 | enabled | Vault-wide task queries | "Tasks due from earlier" in daily notes, Todo Lists index | Single source for task views | Core search for `- [ ]` |
| obsidian-kanban | Kanban | 2.0.51 | enabled | Board view of a note | Todo Lists boards | Boards are plain Markdown lists | Read the board note as a Markdown list |
| tag-wrangler | Tag Wrangler | 0.6.5 | enabled | Rename/merge tags safely | Project-tag convention (`#Projects/…`) | Prevents tag drift breaking roll-ups | Core find-and-replace across files |
| obsidian-linter | Linter | 1.32.0 | enabled | Tidy formatting on demand | Consistent frontmatter shape (manual run only; never on save) | Keeps properties in the validator's YAML subset | Fix properties in the Properties panel |
| table-editor-obsidian | Advanced Tables | 0.23.2 | enabled | Table editing | Parameter tables in experiment templates | Faster table editing than core | Core table editing |
| obsidian-git | Git | 2.39.0 | opt-in | Sync and history through Git/GitHub | Multi-device sync and version history | Network access → opt-in (enable during Day-1 sync setup) | Git command line or GitHub Desktop |
| obsidian-zotero-desktop-connector | Zotero Integration | 3.2.1 | opt-in | Import Zotero annotations and citations | Literature workflow (`Zotero_PDF_notes/`) | Talks to the local Zotero app and uses a native helper → opt-in; desktop only | Export notes from Zotero and paste them |

## Removed in 2.0.0

These plugins were part of the 1.x vault (then called Lab Vault) and were removed to simplify the vault. Do not
reinstall them in the lab template; you may add them to your personal vault at your own risk.

| Plugin id | Name | What to use instead |
|-----------|------|---------------------|
| calendar | Calendar | Core *Open today's daily note* (ribbon/command) and the calendar on Home |
| omnisearch | Omnisearch | Core search (`Ctrl/Cmd+Shift+F`); search PDFs in Zotero |
| obsidian-pandoc-reference-list | Pandoc Reference List | Zotero Integration citations and citekey-named literature notes |
| obsidian-icon-folder | Iconize | Retired (cosmetic only) |
| ob-table-enhancer | Table Enhancer | Advanced Tables and core table editing |
| inline-admonitions | Inline Admonitions | Core callouts (`> [!note]`) |
| obsidian-mind-map | Mind Map | Core Canvas |
| obsidian-local-rest-api | Local REST API | Retired (local server is a security risk) |
| terminal | Terminal | Your system terminal |
| x-post-saver | X Post Saver | Retired (not lab record-keeping) |
| obsidian-google-calendar | Google Calendar | Retired (was installed but never enabled) |
