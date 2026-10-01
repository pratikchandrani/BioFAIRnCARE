---
type: guide
id: new-student-guide
title: "New student note-taking guide"
description: "Step-by-step guide to daily notes, experiment records and the other record types."
created: 2026-08-23
updated: 2026-10-02
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
aliases:
  - onboarding guide
  - note-taking guide
  - student guide
  - start here
---

#PClab/NoteTaking #Concepts/Obsidian #Concepts/Zettelkasten

# Lab Note-Taking Guide - Start Here

Welcome. This vault is your lab notebook and your second brain: daily logs, experiments, samples,
protocols, literature notes and ideas, all as plain Markdown files connected by links, tags and
properties. It follows the **FAIR** principles (findable, accessible, interoperable, reusable) and
the **CARE** principles (collective benefit, authority to control, responsibility, ethics). This
guide gets you from zero to your first daily note and first experiment record in about 30 minutes.

Read it once fully, then keep it open as a reference for your first few weeks. See also
[[Obsidian guide]] for video tutorials and device-sync setup, the [[FAIR guide]], the
[[CARE guide]] and the [[Data capture guide]].

> [!tip] The one habit that matters most
> **Everything starts in today's daily note.** If in doubt about where to write something, write
> it in today's daily note first. When it is an experiment, press **New experiment** from there —
> the daily note and the experiment record stay linked to each other.

---

## 1. What Obsidian is, in one paragraph

Obsidian is a text editor for a folder of `.md` (Markdown) files — that folder is called a
**vault**. It adds **`[[wikilinks]]`** between notes, **properties** (structured fields at the top
of a note), a **graph view**, and a small set of plugins (Dataview, Templater, Tasks, …) that turn
plain text into live tables and one-click commands. Nothing is locked into a proprietary format:
every note is a `.md` file you could open in Notepad.

### Getting set up
1. Install Obsidian ([obsidian.md](https://obsidian.md)) on your laptop.
2. Get your **own private copy** of the lab template (do **not** use *Fork* — a fork of a public
   repository cannot be made private): follow *Setup Git and get the template* in [[Obsidian guide]].
3. **Open folder as vault** → select your vault folder.
4. Obsidian asks to trust the community plugins configured in `.obsidian/` — click **Trust author
   and enable plugins**. Eight plugins switch on automatically; **Git** and **Zotero Integration**
   are opt-in (you enable them in steps 6 and §7). Home opens now, and at every launch from then on.
5. Open [[Vault settings]] and fill in `owner` (your full name) and `owner_initials` (2–4 capital
   letters). Ask the vault maintainer to add you to [[Lab members]] with the same initials — the
   commands use them in every record ID.
6. For syncing your work through Git across devices, follow [[Obsidian guide]] (enable the Git
   plugin there).

### The three editing modes
- **Live Preview** (default) — formatting renders as you type. Use this day to day.
- **Source mode** — raw Markdown always visible. Useful when something does not render.
- **Reading view** — fully rendered, read-only.

The commands (New experiment, Log to experiment, New record, …) insert a link at your cursor. The
**buttons** in daily notes and on Home handle this for you: they switch the note to editing mode
(Home opens today's daily note first). If you use a **hotkey or the command palette** and see
*"No active editor"*, click into a note in editing mode (`Ctrl/Cmd+E` toggles Reading view) and
run the command again.

### Essential moves
| Action | How |
|--------|-----|
| Open today's daily note | Calendar icon in the left ribbon, `Ctrl/Cmd+P` → "Daily notes: Open today's daily note", or click a day on the Home calendar. If today's note exists, it simply opens — there is only ever one note per day |
| Start an experiment record | **New experiment** button in the daily note or `Ctrl/Cmd+Alt+E` — creates a separate note and adds `- Performed [[…]]` to the daily note. Don't use Templater's own "Insert template" for experiments: it only lists the daily template and the lab commands |
| Add to an experiment's progress log | **Log to experiment** or `Ctrl/Cmd+Alt+L` |
| Create a sample, material, protocol, data/code reference, project, concept, event | **New record** or `Ctrl/Cmd+Alt+R` |
| Create a link to another note | Type `[[` and start typing the note name |
| See what links to this note | **Backlinks** pane (right sidebar) |
| Search everything | `Ctrl/Cmd+Shift+F` (core search) |
| Command palette (do anything) | `Ctrl/Cmd+P` |
| Paste an image | `Ctrl/Cmd+V` — it is saved in `files/`; then rename it (see §8) |
| Check your vault | Open [[Vault Health]] |

---

## 2. Markdown basics

You don't need to memorise this — Live Preview shows the result immediately:

```markdown
# Heading 1
## Heading 2

**bold**   *italic*   ==highlight==   ~~strikethrough~~

- bullet list
  - nested bullet
1. numbered list

- [ ] an open task
- [x] a completed task

> A blockquote

[[Concepts/Apoptosis]]           → link to another note in the vault
[[Concepts/Apoptosis|apoptosis]] → same link, displayed as "apoptosis"
![[EXP-AB-20261001-01_gel_20261001.png]] → embed an image stored in the vault
[External link text](https://example.com)

`inline code`

| Table | Header |
|-------|--------|
| cell  | cell   |

#tag-name              → a flat tag
#Projects/YourProject  → a hierarchical tag

---                    → horizontal rule
```

**Callouts** (styled boxes) are built in:

```markdown
> [!note] Optional title
> Content here

> [!warning]
> Something to be careful about
```
Common types: `note`, `tip`, `warning`, `example`, `question`, `quote`.

**Properties** are the fields between the two `---` lines at the top of a note (e.g. `status`,
`projects`, `outcome`). Edit them in the Properties panel; the commands fill most of them for you.

---

## 3. How this vault is organised

| Folder | Purpose |
|--------|---------|
| `daily_notes/` | One file per day, `YYYY-MM-DD.md`. **The entry point for everything you do.** |
| `Experiments/` | One note per experiment (`EXP-…`), created with *New experiment* |
| `Protocols/` | Versioned protocols (`PRT-…`), one note per version |
| `Samples/` | De-identified samples and aliquots (`SMP-…`) |
| `Materials/` | Cell lines, antibodies, reagents, kits, plasmids, primers (`MAT-…`) and instruments (`INS-…`) |
| `Data/` | References to large/raw data (`DATA-…`) and code (`CODE-…`) kept outside the vault |
| `Projects/Auto_summary/` | One project note per project, compiling itself from your daily notes (§6) |
| `Concepts/` | Permanent notes for recurring topics, techniques, genes, pathways |
| `Events/` | Journal clubs, Wonder of the Week, conferences, talks |
| `Todo Lists/` | Kanban boards and long-running checklists |
| `Zotero_PDF_notes/` | Literature notes imported from Zotero, by citekey |
| `files/` | Your attachments (small files only, named by record ID) |
| `Resources/` | Lab-owned, updated by lab releases: `templates/` (daily note + lab commands), `note-templates/` (experiment and record templates; your customised copies in `note-templates/local/`), guides, registers, tools |
| `_Examples/` | Fictional worked examples — read them, then delete the folder |

Every area has an `_Index` note, and [[Home]] links to all of them.

---

## 4. Daily notes — your main workflow

Start a daily note every day you work, and write what you are doing as you go.

### Creating today's note
Ribbon calendar icon, `Ctrl/Cmd+P` → "Daily notes: Open today's daily note", or click today on
the Home calendar. It is created from `Resources/templates/daily.md` with: properties (date,
owner, projects), **Tasks due from earlier**, a short **FAIR reminder**, the **New experiment /
Log to experiment / New record** buttons, **Daily work updates** … **End of daily work updates**,
**Experiments touched today** and **List of notes in past week**. Write your day between "Daily
work updates" and "End of daily work updates".

Rules of thumb:
- **One tag block per project/topic you touched that day**, starting with its tag on its own line
  (e.g. `#Projects/G4Quadruplex`), followed by bullet points.
- **Link out, don't duplicate.** Techniques, genes and concepts get their own notes — `[[link]]`
  them.
- **Log first, organise later.** A link to a note that does not exist yet is fine; click it later
  to create the note.
- **One daily note per day.** Keep appending to the same note.
- Add the projects you worked on to the `projects` property too; *New experiment* copies them
  into the experiment.

---

## 5. Experiments — from the daily note to a FAIR record

The **daily note is your primary note** (Zettelkasten "fleeting" layer): every day of work starts
there. When you do a specific experiment, you launch its template *from* the daily note; the
experiment becomes its own structured note and the daily note keeps a one-line log entry.

1. In today's daily note, put the cursor inside **Daily work updates** (under the project tag).
2. Click **New experiment** (or `Ctrl/Cmd+Alt+E`), pick the type from the catalogue (type to
   filter, e.g. "pcr"), and give a short title, e.g. *PCR of breast cancer tissues*.
3. A new note `Experiments/PCR of breast cancer tissues_<INI>-<YYYYMMDD>-<NN>.md` opens in a new tab
   (the ending is the experiment's ID without `EXP-`). Your daily note gets exactly one line:
   `- Performed [[PCR of breast cancer tissues_<INI>-<YYYYMMDD>-<NN>]]` — extend it with a short
   note ("…, annealing at 58 °C, gel attached"). The experiment's progress log links back to the day.
   - Cursor not inside *Daily work updates*? The line is added just above *End of daily work updates*.
   - Launched from Home, a project or any non-daily note? The line goes to **today's** daily note
     (created if it does not exist yet); the note you were in is not changed.
   - Catching up on an earlier day? Launch from **that day's** daily note: the line goes there and
     the experiment's `start_date` is that day (its ID still carries today's date — when the record
     was written).
4. Fill it top to bottom as you work: aim, materials (with **lot numbers**), protocol **version**,
   procedure, type-specific parameters, observations, results, interpretation, next steps.
5. On later days, use **Log to experiment** from that day's note: it adds the day to the
   experiment's progress log and adds `- Continued [[…]]` to your daily note. **New record**
   (samples, materials, protocols, data/code references…) adds `- Registered [[…]]`.
6. Failed or negative result? Set `outcome: failed` or `negative` and say why in
   `outcome_reason` — negative results are results.

The [[Experiment catalogue]] lists all 32 templates (A1–G3 plus Z1 generic). Browse your
experiments in [[Experiments/_Index|Experiments]].
Status moves `planned → in-progress → completed → signed-off → archived`.

Every note also has three **OKF** properties ([[OKF guide]]): `title` (filled for you),
`description` — **one sentence** on what you did and found; write it when the experiment is
finished (Vault Health warns if a finished experiment has none) — and `tags` (pre-filled; add
cross-cutting facets such as `lung-cancer`).

Supporting records (**New record**): link them in the experiment's properties — `samples`,
`materials`, `instruments`, `protocols` (only *active* versions), `data_refs`, `code_refs`. One
sample or antibody note is then reused by every experiment that uses it.

---

## 6. Tags and projects — the organising backbone

| Tag pattern | Meaning | Example |
|-------------|---------|---------|
| `#Projects/ProjectName` | Work on a specific project | `#Projects/LUADGenomicsLandscape` |
| `#JC` | Journal Club entry | `#JC: deep learning viral DNA in TCGA…` |
| `#WoW` | "Wonder of the Week" entry | `#WoW: non-canonical TCA cycle…` |
| `#Concepts/Topic` | Cross-references a concept area | `#Concepts/GatewayCloning` |

**Use an existing project tag if one exists** — check the [[Projects/Auto_summary/_Index|Project
index]] first. To start a new project: **New record → project** with a short tag name (no spaces),
then use `#Projects/<name>` in your daily notes. The project note compiles every tagged daily
block automatically (newest first) and lists every experiment whose `projects` property links it.
Structured records (experiments, samples, data) link projects in their `projects` property; daily
notes keep using tags.

To see every tag and how often it is used, open [[MoM/Table of Tags|Table of Tags]]. Rename or
merge tags with **Tag Wrangler** (right-click a tag in the Tags pane).

---

## 7. Concept notes and literature

A **Concept note** is a reusable reference note for something you come back to: a technique, a
gene/pathway, software, an idea — the "permanent note" layer of a Zettelkasten (see
[[Obsidian guide]]). Create one with **New record → concept** the second time you find yourself
explaining the same thing in a daily note. Put synonyms in its `search_terms` property; the note
lists every daily note that mentions them, so you never maintain that list by hand. Browse them in
[[Concepts/_Index|Concepts]].

**Literature workflow**
1. Read and annotate in Zotero (colour taxonomy in [[Obsidian guide]]).
2. Enable **Zotero Integration** once (opt-in, desktop only), then import annotations with
   `Ctrl/Cmd+P` → Zotero Integration commands; notes land in `Zotero_PDF_notes/`, named by citekey.
   Without Zotero, use **New record → literature note**.
3. Log the read in your daily note under the project tag, with a link to the literature note.
4. If the paper introduces a concept you will reuse, create or extend the concept note.

---

## 8. Files and data

- **Small files** (≤ 10 MB, open formats — images, PDF, CSV): paste or drag into the experiment;
  they go to `files/`. Rename them `<ID>_<short-description>_<YYYYMMDD>.<ext>` (right-click →
  Rename; links update automatically).
- **Large or raw data** (sequencing, microscopy stacks, `.fcs`, mass-spec, models): never in the
  vault. Keep them in lab storage and create a **data reference** (New record) with location,
  size, checksum, steward and access conditions. Code and notebooks get a **code reference** with
  the exact commit.
- **Never** put patient names, hospital/UHID numbers, phone numbers or dates of birth in any note —
  only de-identified sample codes. For human or community-derived material set
  `human_or_community_data: true` and fill the CARE fields ([[CARE guide]]).

Details: [[Data capture guide]].

---

## 9. Templates and customising

Every template has a version and a change history, and every note records which template and
version it came from. If a template does not fit your work, run **Customise template**
(`Ctrl/Cmd+Alt+T`): you get your own copy in `Resources/note-templates/local/` (recorded with your name,
date and what you changed), and the commands use your copy from then on. Never edit the lab
templates themselves — lab updates replace them. See the [[Template register]].

---

## 10. Review and sign-off

1. When an experiment is finished, set `status: completed`, `end_date` and `outcome`, then run
   **Request review** (`Ctrl/Cmd+Alt+V`) and sync (commit + push).
2. Your PI/mentor (a reviewer in [[Lab members]]) opens your repository, checks the record, fills
   `signed_off_by` and `signed_off_on`, sets `status: signed-off` and commits **under their own
   Git identity**. You never fill the sign-off fields yourself.
3. After sign-off the record is frozen: add corrections only under **Amendments** as
   `- YYYY-MM-DD — Name — what changed and why`.

The validator checks that a listed reviewer made the sign-off commit and that nothing above
*Amendments* changed afterwards.

---

## 11. Tasks

Any line starting with `- [ ]` anywhere in the vault is a task tracked by the **Tasks** plugin;
mark it done with `- [x]`. Your daily note's "Tasks due from earlier" lists every open task, so
jotting `- [ ] re-run alignment with new reference` in a daily entry is enough. Long-running
checklists and Kanban boards live in [[Todo Lists/_Index|Todo Lists]].

---

## 12. Plugin cheat-sheet

| Plugin | What it is for here |
|--------|---------------------|
| **Dataview** | Live tables and lists: Home, project roll-ups, concept back-lists, Table of Tags, Template register, Vault Health |
| **Templater** | Daily template and the lab commands (New experiment, Log to experiment, New record, Customise template, …) |
| **Homepage** | Opens [[Home]] at start-up |
| **Tasks** | Vault-wide `- [ ]` tasks |
| **Kanban** | Board view for notes in Todo Lists |
| **Tag Wrangler** | Rename/merge tags safely |
| **Linter** | Tidy a note's formatting on demand (`Ctrl/Cmd+P` → Linter) — never automatic |
| **Advanced Tables** | Easier table editing |
| **Git** *(opt-in)* | Sync and history through your private GitHub repository — [[Obsidian guide]] |
| **Zotero Integration** *(opt-in, desktop)* | Import Zotero annotations and citations |

Registers and indexes that need no plugin use Obsidian's built-in **Bases**. Full list with
fallbacks: [[Plugin register]].

---

## 13. House rules

- **Log in the daily note the day it happens.** Backfilling weeks later breaks provenance.
- **Start every work block with its project tag**, and add the project to `projects`.
- **Create records with the commands**, never by copying templates — the IDs and links depend on it.
- **Prefer linking over duplicating.** Explaining the same thing twice? Make it a concept note.
- **Don't rename or move notes casually** — Obsidian updates links when you rename inside
  Obsidian; check backlinks afterwards.
- **Keep raw data out**, register it instead; **no participant identifiers, ever.**
- **Check the Project index before creating a new project tag.**
- **Ask before changing `.obsidian/` settings or plugins** — they are lab-owned and replaced by
  lab updates. Your own changes belong in your notes and in `Resources/note-templates/local/`.

---

## 14. Day-1 checklist

- [ ] Install Obsidian, open your **private** vault, trust the plugins
- [ ] Fill [[Vault settings]]; make sure your initials are in [[Lab members]]
- [ ] Enable **Git** and set up sync ([[Obsidian guide]]); enable **Zotero Integration** if you use Zotero
- [ ] Open today's daily note and write one real entry under a project tag
- [ ] Click **New experiment**, pick *Z1 Generic experiment*, and fill the first sections
- [ ] Walk through `_Examples/` (start with its README), then delete the folder when ready
- [ ] Browse the [[Projects/Auto_summary/_Index|Project index]] and the [[Experiment catalogue]]
- [ ] Open [[Vault Health]] — it should show nothing to fix
- [ ] Bookmark this note

Questions on anything here → ask a senior lab member.
