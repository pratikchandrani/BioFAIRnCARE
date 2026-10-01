---
type: guide
id: okf-guide
title: "OKF guide"
description: "What the Open Knowledge Format is, how your notes follow it, and how the lab exports knowledge safely."
tags:
  - guide
  - okf
created: 2026-10-02
updated: 2026-10-02
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

# OKF guide — knowledge that other tools can read

The lab follows three guides together:

| Guide | Question it answers | Where |
|-------|---------------------|-------|
| **FAIR** | Can someone find and reuse this record? | [[FAIR guide]] |
| **CARE** | Are the people and communities behind the data respected? | [[CARE guide]] |
| **OKF** | Can another tool or an AI agent read this knowledge without rewriting it? | this guide |

**OKF** (Open Knowledge Format, version 0.2) is an open specification published by Google Cloud
in 2026. It describes knowledge as a **folder of Markdown files with YAML properties** — exactly
what this vault already is. It is *a format, not a platform*: no account, no app, no upload.
Official text: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

OKF is **not** a data repository, not a licence, and not a reason to share anything. CARE and
confidentiality decide what may leave the lab; OKF only decides *how it is written* when it does.

## The three OKF rules (and how the vault meets them)

1. **Every Markdown note has properties (YAML frontmatter).** Every note you create from a
   command or template has them; so do the guides, Home, README, CHANGELOG and UPGRADE.
2. **Every note has a non-empty `type`.** Your notes have `type: daily`, `experiment`, `sample`,
   `protocol`… — already required by the lab schema.
3. **`index.md` and `log.md` are reserved names.** OKF uses them for folder listings and change
   history, so never name your own notes `index` or `log` (the vault uses `_Index` instead).

*Vault Health* checks all three (rules **OK001**, **OK002**).

## The three properties you fill

Besides `type`, OKF recommends three properties. The templates add them for you:

| Property | What to write | Filled by |
|----------|---------------|-----------|
| `title` | The human name of the note | automatically (experiment title, record name, date) |
| `description` | **One sentence**: what the note is about — for an experiment, what you did and what you found | **you** |
| `tags` | Short cross-cutting facets, lowercase with hyphens | pre-filled (`experiment`, `nucleic-acids`…); add facets such as `lung-cancer` |

Missing `title` or `description` is only a suggestion (**OK003**) — except a **finished
experiment without a description**, which shows a warning (**OK004**): that is the moment you
know the result, so write the sentence then.

### Writing a good description

- ✅ "PCR of TP53 exons 5–6 from A549 genomic DNA; no amplicon and the positive control also failed, so the primer stock is suspected."
- ✅ "Western blot detecting p53 (beta-actin control) in A549 lysates before TP53 knockdown; transfer extended to 75 min."
- ❌ "PCR" (says nothing a reader does not already know from the type)
- ❌ "See results below" (a description must stand on its own)
- ❌ A sample code, patient detail or anything confidential — the description is the part most
  likely to be shown to other tools.

Keep it under 200 characters, one sentence, no links.

## How your notes map to OKF

The vault stays optimised for working in Obsidian (wikilinks, lab statuses). When knowledge is
exported, each property is translated:

| In your note | In the OKF export | Notes |
|--------------|-------------------|-------|
| `type` | `type` | unchanged |
| `title`, `description`, `tags` | `title`, `description`, `tags` | inline `#tags` are added to `tags` |
| `status` | `status` (`draft`, `stable` or `deprecated`) + `lab_status` (your original value) | see the table below |
| `owner`, `updated` | `generated: {by: human:<initials>, at: <date>}` | who wrote it and when |
| `ai_assisted: true` + `ai_note` | `generated.assisted_by` | AI help stays visible |
| `location` (data reference), `repository` (code reference) | `resource` | only when it is a URL or DOI |
| `[[wikilinks]]` | `[Title](/Folder/Note.md)` links | links to notes that are not exported are removed |
| Dataview / Tasks / Bases blocks | a one-line note | dynamic views do not travel |

| In your note | In the OKF export | Notes |
|--------------|-------------------|-------|
| `signed_off_by` + `signed_off_on` | `verified: [{by: human:<reviewer initials>, at: <date>}]` | OKF calls this the **human-reviewed** trust tier |

**Lab status → OKF status**

| Note type | → `draft` | → `stable` | → `deprecated` |
|-----------|-----------|------------|----------------|
| experiment | planned, in-progress | completed | archived |
| protocol | draft | validated, active | superseded, retired |
| daily, event | open / planned | done | — |
| project, literature | — | active, paused, completed, unread, read | archived |
| sample, material, instrument, data/code reference, concept, index, guide | — | active | archived |

A `signed-off` experiment is also `stable` (and gets `verified`).

## Worked example: one experiment, two views

In the vault (properties of the example `_Examples/Experiments/TP53 exon PCR_EX-20260113-01.md`, shortened):

```yaml
type: experiment
id: EXP-EX-20260113-01
title: TP53 exon PCR
description: "PCR of TP53 exons 5–6 from A549 genomic DNA; no amplicon and the positive control also failed, so the primer stock is suspected."
tags: [experiment, nucleic-acids, lung-cancer]
status: completed
owner: Example Student
updated: 2026-01-13
outcome: negative
materials: ["[[MAT-EX-20260105-01 A549 cell line]]"]
```

In the OKF export (same note, shortened):

```yaml
type: "experiment"
title: "TP53 exon PCR"
description: "PCR of TP53 exons 5–6 from A549 genomic DNA; no amplicon and the positive control also failed, so the primer stock is suspected."
tags: ["experiment", "nucleic-acids", "lung-cancer"]
status: "stable"
lab_status: "completed"
generated:
  by: "human:EX"
  at: "2026-01-13T00:00:00Z"
outcome: "negative"
materials: ["/_Examples/Materials/MAT-EX-20260105-01%20A549%20cell%20line.md"]
```

The full, current output of the export for the examples is in `_Examples/OKF/OKF export example.md`
(regenerated with every BioFAIRnCARE release).

## Exporting: who, when, and what never leaves

- **Who**: the export is a Python tool for the **PI or vault maintainer**
  (`Resources/tools/okf_export.py`). Students do not need to run it — ask your PI when a
  collaborator, a lab knowledge base or an AI tool needs the lab's curated knowledge.
- **What it writes**: a *separate* folder (an OKF "bundle"); your vault is never changed. Every
  folder gets an `index.md`, the root declares `okf_version: "0.2"`, and a `log.md` lists the
  history.
- **Always left out**: notes marked `confidential` or `embargoed`; templates, tools and settings.
- **Left out unless the PI asks for a lab-internal export**: notes marked `internal`.
- **Left out unless the PI allows it**: notes with `human_or_community_data: true`. Only the PI
  sets `okf_export: allowed` on such a note, after checking its ethics approval, consent scope and
  sharing restrictions ([[CARE guide]]). It never overrides `confidential` or `embargoed`.
- Left-out notes do not leave a trace: links to them become plain text and their names are listed
  only in a report *next to* the bundle, for the PI.
- Sending a bundle to an external AI service is still governed by institutional policy and the
  constitution (no identifiable or unpublished data).

For maintainers:

```text
python Resources/tools/okf_export.py <vault> <output folder> [--internal] [--examples]
```

## Self-check

1. What are the three OKF conformance rules?
2. Which of your properties does OKF *require*, and which three does it *recommend*?
3. Why must you never call a note `index` or `log`?
4. Write a one-sentence description for a western blot that failed because of a transfer problem.
5. Your note has `human_or_community_data: true` and `confidentiality: public`. Will it be exported? Who could change that?
6. A note is `confidential` and has `okf_export: allowed`. Is it exported?
7. What happens to a wikilink that points to a note that is not exported?
8. In the export, what does `status: draft` tell an OKF reader about a `planned` experiment?

> [!question]- Answers
> 1. Every non-reserved Markdown file has YAML properties; every one has a non-empty `type`;
>    `index.md` / `log.md` follow OKF's structure.
> 2. Required: `type`. Recommended: `title`, `description`, `tags`.
> 3. OKF reserves those names for folder listings and change history; a note with that name
>    would be misread (Vault Health rule OK002).
> 4. For example: "Western blot of p53 in A549 lysates; no bands because transfer failed (Ponceau
>    showed an empty membrane) — repeat planned."
> 5. No — human or community data is left out by default. Only the PI can allow it, by setting
>    `okf_export: allowed` after checking the CARE fields.
> 6. No — `confidential` and `embargoed` always stay in the lab.
> 7. It becomes plain text (its alias, or "(link removed)"), so the name of the left-out note is
>    never revealed.
> 8. That the content is not final yet and may be incomplete (`lab_status: planned` keeps the detail).

## See also

[[FAIR guide]] · [[CARE guide]] · [[Vault Health]] · [[New Student Note-Taking Guide]]
