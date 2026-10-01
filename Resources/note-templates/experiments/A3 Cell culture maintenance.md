<%*
/* TEMPLATE-INFO
template_id: TPL-A3
name: Cell culture maintenance, passaging & cryopreservation
category: A. Biospecimens & materials
version: 1.1.0
status: active
lab_owned: true
original_author: Pratik Chandrani
original_date: 2026-10-01
source_release: Lab Vault 2.0.0
base_template_id:
base_version:
customised_by:
customised_on:
customisation_summary:
CHANGELOG
| version | date       | author           | summary |
|---------|------------|------------------|---------|
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Initial template |
| 1.1.0   | 2026-10-02 | Pratik Chandrani | Add OKF fields description and tags |
END TEMPLATE-INFO */
const settingsFile = app.vault.getAbstractFileByPath("Resources/Vault settings.md");
const settings = (settingsFile && app.metadataCache.getFileCache(settingsFile)?.frontmatter) || {};
const ctx = window.labvaultContext || {};
const today = tp.date.now("YYYY-MM-DD");
const m = tp.file.title.match(/^(.*)_([A-Z]{2,4}-\d{8}-\d{2})$/);
const id = ctx.id || (m ? "EXP-" + m[2] : "");
const title = String(ctx.title || (m ? m[1] : tp.file.title)).replace(/"/g, "'");
const startDate = ctx.start_date || today;
const yamlList = (items) => (items && items.length) ? "\n" + items.map(l => '  - "' + l + '"').join("\n") : "[]";
const projects = yamlList((ctx.projects || []).map(p => String(p).startsWith("[[") ? p : "[[" + p + "]]"));
const origin = ctx.origin || today;
const PROCS = ["maintenance", "thawing", "passaging", "counting", "freezing"];
let procs = [];
while (true) {
  const labels = PROCS.map(p => (procs.includes(p) ? "☑ " : "☐ ") + p).concat(["✔ Done"]);
  const pick = await tp.system.suggester(labels, PROCS.concat(["__done"]), false, "Cell culture: which procedures did you do? Pick to toggle, then Done");
  if (!pick || pick === "__done") break;
  procs = procs.includes(pick) ? procs.filter(p => p !== pick) : procs.concat([pick]);
}
if (!procs.length) procs = ["maintenance"];
const procYaml = "\n" + procs.map(p => "  - " + p).join("\n");
-%>
---
type: experiment
id: <% id %>
title: "<% title %>"
description:
tags:
  - experiment
  - biospecimens-materials
experiment_type: A3
created: <% today %>
updated: <% today %>
start_date: <% startDate %>
end_date:
status: planned
owner: <% settings.owner || "" %>
contributors: []
projects: <% projects %>
protocols: []
samples: []
materials: []
instruments: []
data_refs: []
code_refs: []
outcome: pending
outcome_reason:
literature: []
procedures: <% procYaml %>
human_or_community_data: false
animal_study: false
biosafety_level: BSL-1
ibsc_approval:
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
review_requested: false
signed_off_by:
signed_off_on:
template_id: TPL-A3
template_version: 1.1.0
---
# <% title %>

%% description (in Properties): one sentence — what you did and why; add the result when finished. %%

> [!info] Cell culture maintenance, passaging & cryopreservation · `<% id %>`
> Routine culture, passaging and freezing of a cell line.
> Fill the sections top to bottom as you work. Link records in the properties (protocol
> **version**, samples, materials, data/code references). Small files (≤ 10 MB, open formats) go
> in `files/` named `<% id %>_<short-description>_YYYYMMDD.ext`; large or raw data stays in lab
> storage and gets a **DATA-** reference (*New record → data reference*). Guides: [[Data capture guide]],
> [[FAIR guide]].

## Aim / hypothesis

## Materials

| Material | Identifier (RRID / ontology / Addgene) | Supplier | Catalogue no. | Lot no. | Note |
|----------|----------------------------------------|----------|---------------|---------|------|
|          |                                        |          |               |         |      |

Link the material records (MAT-/INS-) in the `materials` / `instruments` properties.

## Samples

Link sample records (SMP-) in `samples`. Use de-identified codes only — never names, hospital
numbers or dates of birth.

## Protocol and deviations

- Protocol version used: link the PRT- note in `protocols` (only `active` versions).
- Deviations from the protocol (what, why):

## Procedure

1.

## Aseptic pre-work

| Check | Done (✓) |
|-------|----------|
| Hands sanitised, gloves on |  |
| Head cap and dedicated cell-culture lab coat |  |
| Hood wiped with 70 % ethanol and UV ≥ 15 min |  |
| CO₂ incubator checked: ___ °C, ___ % CO₂ |  |
| Water bath at 37 °C |  |
| Medium pre-warmed and labelled |  |
| Sterile pipettes, tubes and tips inside the hood |  |
| Dedicated footwear / shoe covers |  |
| No bacterial work done today before cell culture |  |

## Reagents and media

| Reagent | Material record | Stock conc. | Final conc. | Volume / reaction (µL) | Lot no. |
|---------|-----------------|-------------|-------------|------------------------|---------|
| Base medium (DMEM / RPMI / …) |  |  |  |  |  |
| FBS (e.g. 10 %) |  |  |  |  |  |
| Antibiotic (e.g. 1× Pen-Strep) |  |  |  |  |  |
| Trypsin-EDTA (e.g. 0.25 %) |  |  |  |  |  |
| PBS (1×) |  |  |  |  |  |
| Trypan blue |  |  |  |  |  |

Storage: medium 4 °C, FBS −20 °C (aliquots), trypsin 4 °C / −20 °C (typical — confirm with protocol) — record the actual
storage in each material record.

<%* if (procs.includes("maintenance")) { -%>
## Medium preparation

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Base medium |  |  |  |
| Add FBS aseptically |  |  | e.g. 10 % |
| Add antibiotics |  |  | e.g. 1× Pen-Strep from 100× stock |
| Mix gently, aliquot |  |  |  |
| Label bottle |  |  | date, initials, composition |
| Store |  |  | 4 °C |
<%* } -%>

<%* if (procs.includes("thawing")) { -%>
## Thawing

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Vial retrieved from |  |  | LN₂ / −80 °C; box and position |
| Pre-warm complete medium |  |  | 37 °C |
| Rapid thaw |  |  | 37 °C water bath, 1–2 min |
| Transfer into medium |  |  | e.g. 9 mL complete medium |
| Centrifugation (removes DMSO) |  |  | 200–300 × g, 5 min (typical — confirm with protocol) |
| Resuspend pellet |  |  |  |
| Flask type and volume |  |  | e.g. T25 = 5–7 mL, T75 = 12–15 mL |
| Incubation |  |  | 37 °C, 5 % CO₂ |
| Check after 24 h |  |  | attachment, morphology |
<%* } -%>

<%* if (procs.includes("passaging")) { -%>
## Passaging

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Confluency at passage |  |  | %; typically 70–80 % |
| Wash |  |  | PBS, volume |
| Trypsin volume and time |  |  | min |
| Neutralise |  |  | complete medium, ≥ 2× trypsin volume |
| Centrifugation |  |  | 200–300 × g, 5 min (typical — confirm with protocol) |
| Resuspend in fresh medium |  |  |  |
| Split ratio |  |  | e.g. 1:5 / 1:10 |
| Passage number (from → to) |  |  |  |
| Flask labelled |  |  | cell line, passage, date |
<%* } -%>

<%* if (procs.includes("counting")) { -%>
## Cell counting

| Quadrant | Q1 | Q2 | Q3 | Q4 |
|----------|----|----|----|----|
| Live cells |  |  |  |  |
| Dead (blue) cells |  |  |  |  |

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Sample + trypan blue |  |  | e.g. 1:1 or 1:5 |
| Dilution factor |  |  |  |
| Mean live count per large square |  |  |  |

**Cells / mL** = ___  — formula: mean count per large square × dilution factor × 10⁴

**Viability %** = ___  — formula: live ÷ (live + dead) × 100
<%* } -%>

<%* if (procs.includes("freezing")) { -%>
## Freezing

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Centrifugation |  |  | 200–300 × g, 5 min (typical — confirm with protocol) |
| Freezing medium |  |  | e.g. 90 % FBS + 10 % DMSO |
| Cells per vial |  |  | e.g. 1–2 × 10⁶ |
| Volume per vial |  |  | e.g. 1 mL |
| Controlled-rate freezing |  |  | e.g. isopropanol container at −80 °C overnight |
| Transfer to LN₂ |  |  | tank / rack / box / position |
<%* } -%>

## Microscopy

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| 10× objective |  |  | confluence, distribution |
| 40× objective |  |  | morphology detail |
| 100× objective (oil immersion, if used) |  |  |  |
| Morphology |  |  | adherent / rounded / detaching / healthy |
| Image |  |  | files/<ID>_cells_<YYYYMMDD>.png |

## Troubleshooting

| Issue | Observation | Action taken |
|-------|-------------|--------------|
| Contamination |  |  |
| Low growth rate |  |  |
| Detachment / poor adherence |  |  |
| Irregular morphology |  |  |

Mycoplasma testing → use template **A2**. Did a procedure you did not pick at creation? Copy its
table from the A3 template (Resources/note-templates/experiments) and add the value to `procedures`.

## Biosafety

`biosafety_level` (BSL-1 / BSL-2 / BSL-3) and, for BSL-2 or above or recombinant DNA work,
`ibsc_approval`. Follow the linked protocol's safety section.

## Observations

## Results

### Files in the vault

%% Embed small files, e.g. ![[<% id %>_gel_YYYYMMDD.png]] — originals (uncropped, raw) stay in
lab storage; link them below. %%

### External data and code

Link DATA- and CODE- references in `data_refs` / `code_refs`; describe what each contains here.

## Interpretation

## Next steps

## Progress log

- [[<% origin %>]] — created

## Sign-off

> [!warning] Reviewer only
> When the work is complete, the student sets `status: completed`, `end_date`, `outcome` and runs
> **Request review**. The reviewer (PI/mentor listed in [[Lab members]]) checks the record, sets
> `signed_off_by` (their name), `signed_off_on` (date) and `status: signed-off`, and **commits the
> change under their own Git identity**. After sign-off, nothing above *Amendments* may change.

## Amendments

%% After sign-off, add corrections only here, one per line: - YYYY-MM-DD — Name — what changed and why %%
