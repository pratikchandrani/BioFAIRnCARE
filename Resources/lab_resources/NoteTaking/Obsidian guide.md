---
type: guide
id: obsidian-guide
title: "Obsidian guide"
description: "How to install, open and set up Obsidian and the vault's plugins."
created: 2026-08-23
updated: 2026-10-01
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

> [!tip] New to the lab?
> Start with [[New Student Note-Taking Guide]] — it covers Obsidian/Markdown basics, daily notes,
> experiments, tags, concept notes, files and data, and review. This note is a supplementary link
> collection plus the Git setup and device-sync instructions.

- Video tutorial — basic formatting, daily notes, Zettelkasten, Dataview, Git, templates, PDF annotations: https://www.youtube.com/watch?v=WqKluXIra70 This video is enough to get started; the links below go deeper.
- Obsidian basic formatting guide — https://www.epoch-magazine.com/post/epoch-tutorials-an-introduction-to-obsidian
- More technical setup guide — https://www.emilevankrieken.com/blog/2025/academic-obsidian/
- Concepts of Zettelkasten — https://www.aidanhelfant.com/3-days-to-starting-a-zettelkasten-in-obsidian-as-a-student-part-2/ and https://www.aidanhelfant.com/3-days-to-starting-a-zettelkasten-in-obsidian-as-a-student-part-1/
- Obsidian note example for a biological course — https://sparkl.me/blog/ap/obsidian-zettelkasten-mastering-ap-concepts-with-smart-notes/
- Obsidian–Zotero integration — https://www.youtube.com/watch?v=hRCiuycpAIU
- Obsidian Excalidraw (optional add-on, see the end of this note) — https://www.youtube.com/watch?v=P_Q6avJGoWI

## Setup Git and get the template (private repository)

Your vault holds unpublished research and sample information, so it must live in a **private**
repository. Do **not** click *Fork*: GitHub does not allow a fork of a public repository to be
made private.

1. Make a free account on GitHub (use your institutional e-mail if possible).
2. Visit the BioFAIRnCARE repository and either
   https://github.com/pratikchandrani/BioFAIRnCARE/
   - click **Use this template → Create a new repository** (if the button is shown), or
   - use **Import repository** (https://github.com/new/import) with the URL above.
3. Owner: your GitHub account. Repository name: `NameSurname_notes`. Visibility: **Private**.
   Create it.
4. In your new repository: **Settings → Collaborators → Add people** → add your PI/mentor so they
   can review and sign off your experiments.
5. Use your new repository's URL (`https://github.com/<you>/NameSurname_notes`) in the steps below.

#Concepts/Zettelkasten #Concepts/Obsidian
- A Zettelkasten (German for "slip box" or "card index") is a note-taking and knowledge
  management system developed by the German sociologist Niklas Luhmann.
- At its core, a Zettelkasten has three kinds of notes: fleeting notes (quick thoughts — our daily
  notes), literature notes (from books, articles — our Zotero/literature notes) and permanent notes
  (one focal idea, backed by literature notes — our concept and project notes). Daily and
  literature notes connect into project and concept notes over months and years, building a
  knowledge base that compounds over time.
- #PClab/NoteTaking In this lab, the daily note records day-to-day progress as bullet points,
  structured **experiment templates** (PCR, western blot, cell culture, NGS, cloning, xenografts,
  ML …) capture each experiment in a FAIR way, literature notes come from Zotero, and project tags
  plus links let each project note assemble its own history for periodic review.

#Concepts/Obsidian #Concepts/Git
# Syncing your vault across Windows, iPad and Android

The vault syncs through **your private GitHub repository** using the **Git** plugin. Git is
installed in the template but **opt-in** (switched off): you enable it below on each device.

## How it works (read this first)

- **What syncs once you clone/pull:** theme, snippets, hotkeys and the plugin set — all in
  `.obsidian/` and committed to the repository.
- **What does NOT sync, on purpose:** each device's open tabs/pane layout (`workspace.json`,
  `workspace-mobile.json`) and the Git plugin's own `data.json` (your local Git settings). Both are
  git-ignored, so the 10-minute interval is set on each device.
- **Sync engine:** the plugin auto-commits (`vault backup: <date>`), pulls, then pushes with a
  `merge` strategy. Automatic backup commits are fine for everyday notes; when you change templates
  or settings, also make a manual commit with a descriptive message. True conflicts (same lines
  edited on two devices before either synced) appear as `<<<<<<<` markers; resolve them by hand.
- **Mobile constraint:** iPad and Android use the plugin's built-in JavaScript Git, which only
  speaks HTTPS, so authentication everywhere is a GitHub **Personal Access Token (PAT)**.
- **Never paste a token into a note or a settings file that is committed.** The Git plugin stores
  it in its own git-ignored `data.json` (and Windows Git Credential Manager stores it securely).
  The validator flags token-like strings (rule PV002).

## Target settings

Settings → Community plugins → **Git** → options, on every device:

| Setting | Value |
|---------|-------|
| Vault backup interval (auto commit) | `10` (minutes) |
| Auto pull interval | `10` |
| Auto push interval | `10` |
| Pull updates on startup | On |
| Pull before push | On |
| Merge strategy | Merge (not rebase) |
| Commit message | `vault backup: {{date}}` |

---
## 1. One-time: create a GitHub Personal Access Token

One token per device is cleanest (you can revoke one device without affecting the others).

1. GitHub → Settings → Developer settings → **Personal access tokens** → Fine-grained tokens →
   **Generate new token**.
2. Repository access: only your `NameSurname_notes` repository.
3. Permissions: **Contents → Read and write**.
4. Expiration: e.g. 1 year.
5. Generate and copy the token immediately (shown once); treat it like a password. Name tokens
   per device (`notes-windows`, `notes-ipad`, `notes-android`).

---
## 2. Windows PC

1. **Install Git** (git-scm.com) and **Obsidian** (obsidian.md). Make sure Git is on your PATH.
2. Clone your repository where you want the vault to live:

   ```
   git clone https://github.com/<you>/NameSurname_notes.git
   ```

   On the first push, Git Credential Manager asks for authentication: use your GitHub username and
   paste the PAT as the password.
3. Set your identity once (this records who made each commit):

   ```
   git config --global user.name "Your Name"
   git config --global user.email "the e-mail listed for you in Lab members"
   ```
4. Obsidian → **Open folder as vault** → select the cloned folder → **Trust author and enable
   plugins**. Home opens, and from then on it opens at every launch.
5. Settings → Community plugins → find **Git** → switch it **on**, then set the options from the
   table above.
6. Run `Ctrl/Cmd+P` → **Git: Commit-and-sync** once to confirm push/pull works.

---
## 3. iPad / iPhone

1. Install **Obsidian** from the App Store.
2. Create a new vault (any name; it will be replaced) using local storage, **not** iCloud.
3. Settings → Community plugins → turn off Restricted mode → Browse → search **Git** → install →
   enable.
4. Command palette → **Git: Clone an existing remote repo**:
   - Repo URL: `https://<PAT>@github.com/<you>/NameSurname_notes.git`
   - Directory for clone: `.` (vault root)
   - "Does your remote repo contain a .obsidian directory at the root?" → **Yes**
   - When warned about deleting local config → delete local config and plugins
   - Depth: leave blank
5. Restart Obsidian when prompted, trust the plugins, and switch **Git** on again under Community
   plugins (it is opt-in in the template).
6. Set the intervals and toggles from the table above.
7. **iOS caveat:** background execution is restricted — syncing happens while Obsidian is open.
   Open the app before you start (it pulls on start) and it pushes while you work.

Note: **Zotero Integration** is desktop-only and does not load on mobile; everything else does.

---
## 4. Android

Same as iPad, plus:

1. When creating the vault, turn **ON** the "App storage" toggle — otherwise Android's storage
   permissions can make the Git plugin hang during clone.
2. If syncs stop while the app is in the background, exempt Obsidian from battery optimisation:
   Settings → Apps → Obsidian → Battery → **Unrestricted**.

---
## 5. Sanity check across devices

- Edit a test note on one device, sync (or run **Git: Commit-and-sync**), open another device and
  confirm the change appears within ~10 minutes.
- All devices should show the same theme, plugin list and hotkeys; if not, pull again and check
  that plugins are trusted/enabled.
- `<<<<<<<` / `=======` / `>>>>>>>` markers mean a real merge conflict: keep the version you want,
  delete the markers, commit-and-sync.

## 6. Security note

Each PAT is scoped to one repository — still, treat it as a password. If a device is lost or a
token leaks, revoke it in GitHub → Settings → Developer settings → Personal access tokens and
create a new one. Keep the repository **private**.

#Concepts/ObsidianZotero #Concepts/Obsidian
# Zotero–Obsidian workflow: PDF notes and highlights

Full guideline: [[zotero_obsidian_workflow_tutorial.pdf]]

Zotero (bibliography manager + PDF reader) connects to Obsidian through the **Zotero
Integration** plugin by mgmeyers (folder `obsidian-zotero-desktop-connector`). It is installed in
the template but **opt-in** and **desktop only**: Settings → Community plugins → Zotero
Integration → switch on. Highlighting a paper then turns into a linked, searchable note.

## 1. Read and annotate in Zotero with a colour-coded taxonomy

| Colour | Category | Use for |
|--------|----------|---------|
| Red | Skeptical / Disagree | Debunked, questionable or disputed claims |
| Yellow | Core thesis / Highlight | Claims central to the argument; good for summaries |
| Green | Agreed / Direct quotes | Claims you agree with and intend to cite |
| Blue | Connections / Outside ideas | Claims citing other sources or linking to other readings |
| Purple | Chapter / Section headings | Headers, to keep structure on export |
| Pink | Confusion / Questions | Unclear sections or open questions |
| Orange | Definitions | Core terminology |

## 2. What you need

| Tool | Where | Role |
|------|-------|------|
| Better BibTeX | Zotero add-on | Stable citekeys (e.g. `AuthorShortTitleDate`) used as note names |
| Zotero Integration | Obsidian plugin (installed, opt-in) | Queries Zotero, runs the import template, pulls annotations |
| Templater | Obsidian plugin (installed) | Used by the lab's own templates |

Setup notes:
- In Zotero Integration settings, the note import folder is `Zotero_PDF_notes` (already set).
  Create an Import Format with output path `Zotero_PDF_notes/{{citekey}}.md` and bind a hotkey
  (e.g. `Ctrl+Shift+Z`).
- Colour-matched highlight styling in Obsidian (the "Highlighter" plugin used in the tutorial) is
  **not** part of the lab template; install it in your own vault only if you want it.

## 3. The import template

Zotero Integration renders a Nunjucks template that builds the note's properties, a persistent
notes section (kept across re-imports) and the list of highlights with links back to the PDF page.
Re-running the import is non-destructive for anything you write under the persistent section.
Imported notes without lab properties are valid (they show as *legacy* in the validator); add
`type: literature` and `citekey` when convenient, or write literature notes with **New record →
literature note**.

## 4. From source notes to atomic (Zettelkasten) notes

Don't leave literature archived by source. After importing, decompose its arguments into
standalone **concept notes**, one per idea. Before creating one, search the vault for an existing
note and extend it — e.g. one `culture` note collecting how several authors define the term.

## 5. Visualising the graph

- **Local graph** (note menu → Open local graph): 1-depth connections of the active note.
- **Canvas** (core): an infinite whiteboard — drag literature notes, concept notes and diagrams
  onto it, draw arrows, cluster, and zoom out for a chapter or thesis outline.

## 6. Writing: citations in Word / Google Docs

Zotero's word-processor plugin inserts citations in any style and builds the reference list from
everything cited, avoiding missed citations.

#Concepts/ObsidianExcalidraw #Concepts/Obsidian
# Excalidraw in Obsidian: visual note-taking (optional)

Full guideline: [[obsidian-excalidraw-tutorial.pdf]]

Excalidraw is **not installed** in the lab template (to keep the plugin set small). Obsidian's
core **Canvas** covers most diagramming needs (pipelines, experiment overviews, mind maps). If you
want hand-drawn diagrams and PDF sketching, you may install Excalidraw in your own vault; the
tutorial PDF above covers drawing, linking drawings to notes, Mermaid conversion, PDF annotation
and its script store. Keep any drawing that is part of a record as an exported PNG/SVG in
`files/`, so the record stays readable without the plugin.
