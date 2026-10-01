---
type: index
id: feature-preservation-register
title: "Feature preservation register"
description: "Where every 1.x feature (then called Lab Vault) lives in BioFAIRnCARE."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

# Feature preservation register

How every feature of Lab Vault 1.x (publish area at commit `a155a17`) carries into 2.0.0
(spec `001-fair-lab-vault`, success criterion SC-005).

| # | 1.x feature | Status in 2.0.0 | Where it lives now |
|---|-------------|-----------------|--------------------|
| E1 | Home dashboard "PTG's brain": logo, live clock/date, activity calendar, navigation, vault stats, recently modified/created | **Preserved + extended** | [[Home]] — same widgets; navigation now opens every area and the commands; examples/templates excluded from stats; plain quick-links section for use without plugins |
| E2 | Daily note per day with open tasks, "Daily work updates", past-week notes | **Preserved + extended** | `Resources/templates/daily.md` (TPL-DAILY 2.0.0): same sections plus FAIR properties, FAIR reminder, New experiment / Log / New record buttons, experiments touched today; open tasks via Tasks |
| E3 | `#Projects/…`, `#JC`, `#WoW`, `#Concepts/…` tags; project roll-ups; project index | **Preserved + extended** | Project template (TPL-R-PROJECT) compiles tagged daily blocks and lists linked experiments; [[Projects/Auto_summary/_Index|Project index]]; [[MoM/Table of Tags|Table of Tags]]; [[Events/_Index|Events]] lists #JC/#WoW |
| E4 | Concept notes with self-updating "daily notes discussing this concept" | **Preserved** | Concept template (TPL-R-CONCEPT), driven by `search_terms` and aliases; [[Concepts/_Index|Concepts]] |
| E5 | Zotero literature workflow, colour taxonomy, citations | **Preserved (opt-in)** | Zotero Integration plugin installed, opt-in, desktop-only; import folder `Zotero_PDF_notes/`; Literature template; [[Obsidian guide]] |
| E6 | Vault-wide tasks; Todo Lists / Kanban | **Preserved** | Tasks queries in daily notes and [[Todo Lists/_Index|Todo Lists]]; Kanban plugin kept |
| E7 | Multi-device Git sync (Windows, iPad, Android), `.gitignore` | **Preserved (opt-in)** | Git plugin installed, opt-in; [[Obsidian guide]] updated for private repositories and token safety; `.gitignore` extended with raw-data patterns |
| E8 | Onboarding guide, Obsidian guide, Zotero and Excalidraw tutorials | **Preserved + updated** | [[New Student Note-Taking Guide]], [[Obsidian guide]] (Excalidraw marked optional, not installed), tutorial PDFs kept |
| E9 | 12 further plugins (search, tags, tables, mind map, icons, admonitions, linter, REST API, terminal, X saver, calendar, Pandoc list) | **Reduced** | Kept: Tag Wrangler, Linter, Advanced Tables. Replaced or retired: see the [[Plugin register]] ("Removed in 2.0.0") |
| E10 | Folders `daily_notes/`, `Projects/`, `Concepts/`, `Resources/`, `Events/`, `Zotero_PDF_notes/`, `Todo Lists/`, `MoM/`, `files/` | **Preserved + extended** | All kept; added `Experiments/`, `Protocols/`, `Samples/`, `Materials/`, `Data/`, `_Examples/`, `Resources/bases/`, `Resources/tools/`; each area has an `_Index` note |

## Contradictions resolved (spec X1–X15)

- Plugins: 20 → 10 registered (8 enabled, Git and Zotero Integration opt-in) under constitution
  v2.0.0.
- Template folder casing unified (`Resources/templates`); single attachment folder `files/`.
- Public forks → private repositories created from the template; tokens never in versioned files.
- Automatic `vault backup` commits stay for routine notes; structural changes and sign-off
  amendments are committed by hand with descriptive messages.
- Daily notes keep `YYYY-MM-DD.md` names (the date is their ID); records use
  `PREFIX-INI-YYYYMMDD-NN`.
- The guide's "Zotero Integration" is the installed plugin (`obsidian-zotero-desktop-connector`
  is its folder name); Excalidraw and Highlighter were never installed and are now documented as
  optional personal add-ons.
