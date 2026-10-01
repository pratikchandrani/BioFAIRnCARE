<%*
/* TEMPLATE-INFO
template_id: TPL-C6
name: SDS-PAGE & total-protein staining
category: C. Proteins
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
-%>
---
type: experiment
id: <% id %>
title: "<% title %>"
description:
tags:
  - experiment
  - proteins
experiment_type: C6
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
human_or_community_data: false
animal_study: false
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
review_requested: false
signed_off_by:
signed_off_on:
template_id: TPL-C6
template_version: 1.1.0
---
# <% title %>

%% description (in Properties): one sentence — what you did and why; add the result when finished. %%

> [!info] SDS-PAGE & total-protein staining · `<% id %>`
> Separate proteins by SDS-PAGE and stain the gel (Coomassie / silver) without blotting.
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

## Gel recipe

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Resolving gel acrylamide % |  |  |  |
| Resolving buffer |  |  | Tris-HCl pH 8.8 |
| Resolving SDS |  |  | % |
| Resolving APS (10 %) |  |  | µL |
| Resolving TEMED |  |  | µL |
| Stacking gel acrylamide % |  |  |  |
| Stacking buffer |  |  | Tris-HCl pH 6.8 |
| Stacking SDS |  |  | % |
| Stacking APS (10 %) |  |  | µL |
| Stacking TEMED |  |  | µL |
| Gel size and number of wells |  |  |  |

## Samples

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Protein concentration |  |  | µg/µL |
| Sample buffer |  |  | Laemmli 1× |
| Reducing agent |  |  | β-ME / DTT, mM |
| Denaturation |  |  | e.g. 95 °C, 5 min |
| Molecular-weight marker |  |  | name, µL per well |

## Loading map

| Lane | Sample (ID or link) | Protein (µg) | Volume (µL) | Antibody / stain | Expected size (kDa) | Band observed |
|------|---------------------|--------------|-------------|------------------|---------------------|---------------|
| 1 | Ladder |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |
| 6 | Loading / housekeeping control |  |  |  |  |  |
| 7 | Positive control |  |  |  |  |  |

## Electrophoresis

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Resolving gel % |  |  | e.g. 10–12 % |
| Stacking gel % |  |  | e.g. 4–5 % |
| Running buffer |  |  | e.g. 1× Tris-glycine-SDS |
| Voltage / current and time |  |  |  |
| Temperature |  |  | RT / 4 °C |

## Staining

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Stain |  |  | Coomassie / silver / other |
| Fix |  |  | % methanol + % acetic acid, time |
| Stain |  |  | solution, time |
| Destain |  |  | solution, until background clear |

## Imaging

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Imaging system |  |  | link the INS- record |
| Exposure |  |  | seconds; start with auto-exposure (typical — confirm with protocol) |
| Image files |  |  | PNG/JPG preview ≤ 10 MB in files/; raw TIFF or instrument file as DATA- reference |

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
