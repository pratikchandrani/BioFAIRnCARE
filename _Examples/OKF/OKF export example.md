---
type: guide
id: okf-export-example
title: "OKF export example"
description: "What the lab's OKF export produces from the fictional examples, regenerated with every release."
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
example: true
---

# OKF export example

This is the real output of `Resources/tools/okf_export.py` run on the fictional examples
(`--examples --internal`), produced while building this BioFAIRnCARE release. Read it together with
the *OKF guide* (Resources → lab_resources): it shows the bundle's root `index.md`, one exported
experiment, one exported material record and the export report.

Things to notice:

- Wikilinks became links such as `/_Examples/Materials/…md`; dynamic views became a one-line note.
- `status` is the OKF lifecycle value and `lab_status` keeps the vault's value.
- `generated.by` names the author as `human:<initials>`.
- The tumour samples are **not** in the bundle: they hold patient-derived (human) data and the PI
  has not set `okf_export: allowed`. The report counts them but never names them.

%% okf-example:start %%
Export summary: `exported 45 notes, excluded 7 (care:no-export-permission: 5, not-knowledge: 2), attachments 1; OKF v0.2 conformance: OK`

### `index.md`

````markdown
---
okf_version: "0.2"
---
# BioFAIRnCARE knowledge bundle

OKF v0.2 bundle exported from a BioFAIRnCARE vault. Links are bundle-relative; see EXPORT-REPORT.md.

## Folders

* [Concepts](/Concepts/index.md) - 1 note
* [Data](/Data/index.md) - 1 note
* [Events](/Events/index.md) - 1 note
* [Experiments](/Experiments/index.md) - 1 note
* [Materials](/Materials/index.md) - 1 note
* [MoM](/MoM/index.md) - 1 note
* [Projects](/Projects/index.md) - 1 note
* [Protocols](/Protocols/index.md) - 1 note
* [Resources](/Resources/index.md) - 11 notes
* [Samples](/Samples/index.md) - 1 note
* [Todo Lists](/Todo%20Lists/index.md) - 1 note
* [Zotero_PDF_notes](/Zotero_PDF_notes/index.md) - 1 note
* [_Examples](/_Examples/index.md) - 18 notes
* [daily_notes](/daily_notes/index.md) - 1 note

## Notes

* [BioFAIRnCARE changelog](/CHANGELOG.md) - All notable changes to the BioFAIRnCARE template (formerly Lab Vault), newest first.
* [BioFAIRnCARE upgrade notes](/UPGRADE.md) - What to do when you update your vault to a new BioFAIRnCARE version.
* [BioFAIRnCARE — read me](/README.md) - What BioFAIRnCARE is, how to start, and where to find the guides.
* [Export report](/EXPORT-REPORT.md) - How this OKF bundle was produced from a BioFAIRnCARE vault (45 notes).
* [Home](/Home.md) - Start page of BioFAIRnCARE: today's note, quick links, experiments and records at a glance.
````

### `_Examples/Experiments/TP53 exon PCR_EX-20260113-01.md`

````markdown
---
type: "experiment"
title: "TP53 exon PCR"
description: "PCR of TP53 exons 5–6 from A549 genomic DNA; no amplicon and the positive control also failed, so the primer stock is suspected."
tags:
  - "experiment"
  - "nucleic-acids"
  - "lung-cancer"
status: "stable"
lab_status: "completed"
generated:
  by: "human:EX"
  at: "2026-01-13T00:00:00Z"
id: "EXP-EX-20260113-01"
created: "2026-01-13"
updated: "2026-01-13"
experiment_type: "B2"
start_date: "2026-01-13"
end_date: "2026-01-13"
owner: "Example Student"
contributors: []
projects:
  - "/_Examples/Projects/DemoTP53Project.md"
protocols: []
samples: []
materials:
  - "/_Examples/Materials/MAT-EX-20260105-01%20A549%20cell%20line.md"
instruments: []
data_refs: []
code_refs: []
outcome: "negative"
outcome_reason: "No amplicon; positive control also failed → primer stock suspected"
literature: []
human_or_community_data: false
animal_study: false
confidentiality: "internal"
license: "lab-internal"
ai_assisted: false
ai_note:
review_requested: false
signed_off_by:
signed_off_on:
example: true
template_id: "TPL-B2"
template_version: "1.0.0"
---
> [!example] Fictional example — all names, numbers and locations are made up.

# TP53 exon PCR

## Aim / hypothesis
Amplify TP53 exon 5–6 (fictional primers) from A549 gDNA.

## Reaction set-up

| Reagent | Material record | Stock conc. | Final conc. | Volume / reaction (µL) | Lot no. |
|---------|-----------------|-------------|-------------|------------------------|---------|
| Template DNA / cDNA | A549 gDNA (fictional) | 50 ng/µL | 2 ng/µL | 1 | — |
| Forward primer | TP53-ex5-F (fictional) | 10 µM | 0.4 µM | 1 | EX-P-11 |
| Reverse primer | TP53-ex6-R (fictional) | 10 µM | 0.4 µM | 1 | EX-P-12 |
| dNTP mix | | 10 mM each | 0.2 mM | 0.5 | EX-D-03 |
| Polymerase (Taq / high-fidelity) | | 5 U/µL | 0.025 U/µL | 0.125 | EX-T-07 |
| Reaction buffer | | 10× | 1× | 2.5 | EX-T-07 |
| MgCl₂ (if separate) | | 25 mM | 1.5 mM | 1.5 | EX-T-07 |
| Nuclease-free water (to volume) | | | | to 25 | |

Master mix for: 5 reactions (+ 10 % extra for pipetting loss)

- Template source: gDNA · Template concentration: 50 ng/µL

## Thermal cycling

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Initial denaturation | 95 °C | 3 min | |
| Denaturation | 95 °C | 30 s | |
| Annealing | 60 °C | 30 s | |
| Extension | 72 °C | 30 s | 480 bp product |
| Number of cycles | | 35 | |
| Final extension | 72 °C | 5 min | |
| Hold | 4 °C | ∞ | |
| Instrument | | thermocycler (fictional) | |

## Gel check

| Lane | Sample (ID or link) | Type | Amount loaded | Primer pair / probe | Expected size (bp) | Band observed |
|------|---------------------|------|---------------|---------------------|--------------------|---------------|
| 1 | Ladder | DNA | 5 µL | — | — | yes |
| 2 | A549 gDNA rep 1 | DNA | 5 µL | TP53-ex5-F / ex6-R | 480 | no |
| 3 | A549 gDNA rep 2 | DNA | 5 µL | TP53-ex5-F / ex6-R | 480 | no |
| 4 | Negative control | DNA | 5 µL | TP53-ex5-F / ex6-R | — | no |
| 5 | Positive control | DNA | 5 µL | GAPDH primers | 220 | no |
| 6 | NTC (no-template control) | — | 5 µL | TP53-ex5-F / ex6-R | — | no |

1.5 % agarose gel. The positive control also failed, which points to a reagent problem rather
than the TP53 primers.

## Interpretation
No product — a **negative result** is still a result. Likely primer design issue.

## Progress log

- [2026-01-15](/_Examples/daily_notes/2026-01-15.md) — created

## Sign-off

Not yet reviewed (examples are never signed off).

## Amendments
````

### `_Examples/Materials/MAT-EX-20260105-01 A549 cell line.md`

````markdown
---
type: "material"
title: "A549 cell line"
description: "Human lung adenocarcinoma cell line used in the demo project, with its RRID."
tags:
  - "material"
  - "cell-line"
status: "stable"
lab_status: "active"
generated:
  by: "human:EX"
  at: "2026-01-05T00:00:00Z"
id: "MAT-EX-20260105-01"
created: "2026-01-05"
updated: "2026-01-05"
owner: "Example Student"
material_kind: "cell_line"
supplier: "Cell repository (fictional lot)"
catalog_no: "EX-CCL-185"
lot_no: "EX-LOT-0042"
rrid: "CVCL_0023"
identifier: "Cellosaurus CVCL_0023"
storage: "LN2 tank 1 / rack C"
qc_status: "authenticated"
str_authenticated_on: "2026-01-06"
mycoplasma_tested_on: "2026-01-06"
passage_at_receipt: "P12"
projects:
  - "/_Examples/Projects/DemoTP53Project.md"
confidentiality: "internal"
license: "lab-internal"
ai_assisted: false
example: true
template_id: "TPL-R-MATERIAL"
template_version: "1.0.0"
---
> [!example] Fictional example — all names, numbers and locations are made up.

# A549 cell line

Human lung adenocarcinoma cell line used in the demo project.
````

### `EXPORT-REPORT.md`

````markdown
---
type: "guide"
title: "Export report"
description: "How this OKF bundle was produced from a BioFAIRnCARE vault (45 notes)."
---
# Export report

- Exported notes: 45
- Attachments: 1
- Left out: 7 (names are listed only outside the bundle)

| Reason | Notes |
|--------|-------|
| care:no-export-permission | 5 |
| not-knowledge | 2 |

Options: internal=True, examples=True, edition=standard.
````
%% okf-example:end %%
