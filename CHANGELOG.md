---
type: guide
id: changelog
title: "BioFAIRnCARE changelog"
description: "All notable changes to the BioFAIRnCARE template (formerly Lab Vault), newest first."
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

# Changelog — BioFAIRnCARE

All notable changes to the BioFAIRnCARE template (formerly Lab Vault). Versions follow semantic versioning
(MAJOR = breaking folder/plugin/schema change, MINOR = new templates/features, PATCH = fixes).

## [2.1.0] - 2026-10-02

Open Knowledge Format (OKF v0.2) alongside FAIR and CARE (spec `005-okf-compliance`).

### Added
- **OKF properties** in every template: `title` (filled for you), `description` (one sentence you
  write) and `tags` (pre-filled with the note type or experiment category). All 32 experiment and
  10 record templates are now version 1.1.0; the daily template is 2.1.0.
- **OKF guide** (Resources → lab_resources): what OKF is, how your properties map to it, how to
  write a description, what the export leaves out, and a self-check. FAIR, CARE and student guides
  link to it; Home has a quick link.
- **OKF export** `Resources/tools/okf_export.py` (for the PI / maintainer): writes a separate,
  OKF-conformant bundle with Markdown links, OKF status plus `lab_status`, authorship
  (`generated`), a folder `index.md` everywhere and a `log.md`. Confidential and embargoed notes
  never leave the lab, internal notes only with `--internal`, and human / community-data notes only
  when the PI sets `okf_export: allowed`. The vault is never changed.
- `_Examples/OKF/OKF export example.md` shows the real export output, regenerated at every release.
- **Checks OK001–OK004** in the validator and Vault Health: notes need properties with a `type`;
  `index.md` / `log.md` are reserved names; missing title or description is a suggestion; a
  finished experiment without a description is a warning.
- Signed-off experiments are exported with OKF `verified` (human-reviewed trust tier).

### Changed
- **New name: BioFAIRnCARE** (formerly Lab Vault) — "An electronic laboratory notebook (ELN)
  following FAIR and CARE principles and OKF format". Releases now come from
  github.com/pratikchandrani/BioFAIRnCARE (Lite edition: BioFAIRnCARE-lite,
  github.com/pratikchandrani/BioFAIRnCARE-lite). Internal names (validator, scripts, properties,
  IDs) are unchanged.
- **Licence: GNU GPL v3** from this release on (previously MIT; copies received earlier under MIT
  keep that licence).
- README, CHANGELOG and UPGRADE now have properties (`type: guide`), as OKF requires.
- Every guide, index, Home and example now has a title and a one-sentence description.
- The validator's legacy-note warning FM010 is replaced by OK001.

## [2.0.0] - 2026-10-01

**Standard edition** — reviewer sign-off verified against Git history.

FAIR & CARE lab vault for biological research students (spec `001-fair-lab-vault`).

### Added
- **Experiment templates** for 32 cancer-research workflows (A1–G3 + Z1 generic): biospecimens,
  nucleic acids, proteins, cell-based assays, xenografts, exome/RNA-seq/microbiome, modelling,
  ML and exploratory analysis — all sharing one FAIR core and adding type-specific parameters.
- **Bench-level detail** (from a survey of lab-built templates, spec 002): reagent tables with
  stock / final / volume and lot, thermal-cycling and melt-curve tables, gel loading maps with
  explicit controls, a 96-well plate grid (B3, C4, D1, D2), worked calculations with formulas
  (cell count, ΔΔCq, % input, fraction bound, normalised ratio), Ponceau S check and housekeeping
  row in western blots, aseptic checklist and per-procedure step tables in cell culture (A3 asks
  which procedures were done). New templates **B7 ChIP**, **B8 Agarose gel**, **C6 SDS-PAGE &
  staining**, **C7 EMSA**. Doubtful example values are shown only as hints marked
  "typical — confirm with protocol".
- **Record templates**: sample, material, instrument, protocol version, data reference, code
  reference, project, concept, literature, event.
- **Commands** (Templater): New experiment (`Ctrl/Cmd+Alt+E`), Log to experiment (`+L`), New record
  (`+R`), Request review (`+V`), Customise template (`+T`); lab-wide IDs `PREFIX-INI-YYYYMMDD-NN`.
- **Template versioning**: TEMPLATE-INFO block (version, origin, CHANGELOG) in every template;
  `template_id`/`template_version` in every note; local customised copies in
  `Resources/templates/local/`; Template register with "update available".
- **FAIR guide**, **CARE guide**, **Data capture guide**; CARE, animal-ethics and biosafety fields.
- **Registers** (core Bases): experiments, data/code references, samples, materials, protocols.
- **Validator** `Resources/tools/validate_vault.py` (Python stdlib, 46 rules incl. reviewer
  sign-off verified against Git history) and in-Obsidian **Vault Health**.
- `_Examples/` with one fictional worked experiment per category (safe to delete).
- Vault settings, Lab members (initials and reviewers), Plugin register, Feature preservation
  register, `lab-owned.txt` and copy-in update packages.

- **Experiment launch flow** (spec 003): experiments are always separate notes named
  `<Title>_<INI>-<YYYYMMDD>-<NN>.md` (constitution v2.1.0); the daily note gets one log line
  (`- Performed / Continued / Registered [[…]]`) at the cursor or at the end of *Daily work
  updates*; launches from non-daily notes go to today's daily note (created if missing); backfilled
  days set `start_date`. Experiment and record templates moved to `Resources/note-templates/` so
  Templater's "Insert template" lists only the daily template and lab commands. New check LK004
  (experiment not linked from a daily note).

### Changed
- Daily template 2.0.0: FAIR properties and reminder, action buttons, experiments touched today;
  open tasks via the Tasks plugin. Structure of 1.x preserved.
- Home dashboard (was `PTG's brain`): same widgets plus entry points for every area; examples
  and templates excluded from stats; new header image; opens at launch (also before community
  plugins are trusted, via the shipped workspace).
- Template folder path unified to `Resources/templates`; lab logo moved to
  `Resources/lab_resources/assets/`; core Templates disabled (Templater only); Properties enabled.
- Linter runs on demand only (never on save, so finished records are never reformatted).

### Removed
- 11 community plugins: Calendar, Omnisearch, Pandoc Reference List, Iconize, Table Enhancer,
  Inline Admonitions, Mind Map, Local REST API, Terminal, X Post Saver, Google Calendar
  (replacements in the Plugin register). The Inline Admonitions CSS snippet was removed with it.
- Obsidian Git and Zotero Integration are now **opt-in** (installed, switched off by default).

## [1.x] - baseline

- Imported from the publish area `MyName_notes` at commit `a155a17`
  ("Update README to include FAIR and CARE principles") as the starting point for 2.0.0.
