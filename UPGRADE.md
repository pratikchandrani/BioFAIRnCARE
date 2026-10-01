---
type: guide
id: upgrade
title: "BioFAIRnCARE upgrade notes"
description: "What to do when you update your vault to a new BioFAIRnCARE version."
tags:
  - guide
created: 2026-10-01
updated: 2026-10-02
status: active
owner: Lab
confidentiality: public
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Upgrade notes — BioFAIRnCARE

## [2.1.0] - upgrading from 2.0.0

Apply the update package as usual. **None of your notes are changed.**

0. Lab Vault is now **BioFAIRnCARE** (formerly Lab Vault). Nothing in your notes, settings or your
   own Git repository needs renaming. New releases come from
   github.com/pratikchandrani/BioFAIRnCARE (Lite edition: github.com/pratikchandrani/BioFAIRnCARE-lite);
   the old repository (formerly Lab Vault) receives no further updates. The template is now licensed under
   the GNU GPL v3.

1. New notes get the OKF properties `title`, `description` and `tags` automatically. Adding them to
   older notes is optional; Vault Health lists them as *suggestions* only.
2. Write a one-sentence `description` on finished experiments — Vault Health shows a warning for a
   finished experiment without one.
3. Notes **without any properties** (for example notes kept from the 1.x vault, then called Lab Vault) now show **OK001**:
   add a short properties block with at least a `type` (e.g. `type: concept`, `type: literature`)
   — the quickest way is to open the note and add the properties from the matching *New record*
   template. Until then they are simply left out of OKF exports.
4. Never name a note `index` or `log` (OK002); rename such notes if you have them.
5. Need the lab's knowledge as an OKF bundle (for a collaborator, a knowledge base or an AI tool)?
   Ask your PI — see the *OKF guide*.

## [2.0.0] - upgrading from 1.x

Everything you wrote in 1.x keeps working: daily notes, `#Projects/…` tag blocks, concept notes
and Zotero notes stay valid. The validator only shows a *legacy note* warning (FM010) for notes
without the new properties — you never have to migrate them.

### Do once

1. **Back up / commit** your vault.
2. Apply the update package (see its `UPDATE-README.md`), or start from a fresh copy of the
   template and move your own folders across.
3. Delete what the package lists as removed, in particular:
   - `PTG's brain.md` (replaced by `Home.md`)
   - the 11 removed plugin folders in `.obsidian/plugins/` (calendar, omnisearch,
     obsidian-pandoc-reference-list, obsidian-icon-folder, ob-table-enhancer, inline-admonitions,
     obsidian-mind-map, obsidian-local-rest-api, terminal, x-post-saver, obsidian-google-calendar)
   - `.obsidian/snippets/inlineAdmonitionsPluginReadOnly.css`
   - `files/Logo_noBG_20250307.png` (replaced by `Resources/lab_resources/assets/home_page_image_20261001.png`)
4. Fill `Resources/Vault settings.md` (`owner`, `owner_initials`, `pi`) and ask the maintainer to
   list your initials in *Lab members*.
5. Re-enable **Git** (and **Zotero Integration** if you use it) in *Settings → Community plugins*:
   they are opt-in from 2.0.0.
6. If your repository was a public **fork**, move to a **private** repository (GitHub cannot make
   a fork of a public repository private): create a new private repository, push your vault to it,
   and give your PI access — see the Obsidian guide.

### What replaced removed plugins

| Was | Now |
|-----|-----|
| Calendar sidebar | Ribbon / command *Open today's daily note*, or the calendar on Home |
| Omnisearch (`Ctrl/Cmd+Shift+F`) | Core search (same shortcut); search PDFs inside Zotero |
| Pandoc Reference List | Zotero Integration citations; literature notes by citekey |
| Iconize folder icons | Retired (cosmetic) |
| Table Enhancer | Advanced Tables / core table editing |
| Inline Admonitions | Core callouts `> [!note]` |
| Mind Map | Core Canvas |
| Local REST API, Terminal, X Post Saver, Google Calendar | Retired |

### Optional: bring an old note up to 2.0.0

Add the core properties (`type`, `id`, `created`, `updated`, `status`, `owner`,
`confidentiality`, `license`, `ai_assisted`) in the Properties panel. For an old experiment
written in a daily note, the easiest path is: run **New experiment** for it, paste the old text
into the new note, and link the new note from the old daily note.
