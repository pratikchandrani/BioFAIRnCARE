<%*
/* TEMPLATE-INFO
template_id: TPL-B7
name: Chromatin immunoprecipitation (ChIP / ChIP-qPCR)
category: B. Nucleic acids
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
  - nucleic-acids
experiment_type: B7
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
template_id: TPL-B7
template_version: 1.1.0
---
# <% title %>

%% description (in Properties): one sentence — what you did and why; add the result when finished. %%

> [!info] Chromatin immunoprecipitation (ChIP / ChIP-qPCR) · `<% id %>`
> Map protein–DNA interactions at chosen loci by immunoprecipitating crosslinked chromatin.
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

## Sample

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Organism / cell type |  |  |  |
| Treatment / condition |  |  |  |
| Biological replicates |  |  |  |
| Cell count or tissue amount |  |  |  |

## Crosslinking and lysis

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Crosslinking reagent and time |  |  | e.g. 1 % formaldehyde, 10 min |
| Quenching |  |  | e.g. 125 mM glycine, 5 min |
| Lysis buffer |  |  | composition, protease inhibitors |
| Shearing method |  |  | sonication / enzymatic; settings |
| Fragment size check |  |  | e.g. 200–500 bp; run with template B8 and link |

## Immunoprecipitation

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Antibody |  |  | link the MAT- record / RRID |
| Antibody amount |  |  | µg |
| Beads |  |  | protein A/G / magnetic |
| Chromatin per IP |  |  |  |
| Incubation |  |  | time, temperature |
| Control IP |  |  | IgG / no-antibody |
| Wash buffers |  |  |  |
| Number of washes |  |  |  |

## Elution and reverse crosslinking

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Elution buffer |  |  |  |
| Reverse crosslinking |  |  | e.g. 65 °C, 4–6 h |
| RNase / proteinase K |  |  |  |
| DNA purification method |  |  |  |
| Final volume |  |  | µL |
| Storage |  |  | −20 / −80 °C |

## qPCR validation

| Reagent | Material record | Stock conc. | Final conc. | Volume / reaction (µL) | Lot no. |
|---------|-----------------|-------------|-------------|------------------------|---------|
| ChIP / input DNA |  |  |  |  |  |
| Forward primer |  |  |  |  |  |
| Reverse primer |  |  |  |  |  |
| qPCR master mix |  |  |  |  |  |
| Nuclease-free water (to volume) |  |  |  |  |  |

Master mix for: ___ reactions (+ 10 % extra for pipetting loss)

## Results

| Target locus | Cq input | Cq IP | Cq IgG | % input | Fold enrichment over IgG |
|--------------|----------|-------|--------|---------|--------------------------|
|              |          |       |        |         |                          |

**% input** = ___  — formula: 100 × 2^(Cq input adjusted − Cq IP); Cq input adjusted = Cq input − log2(input dilution factor)

**Fold enrichment** = ___  — formula: % input (IP) ÷ % input (IgG)

## Controls

| Control | Locus / sample | Result |
|---------|----------------|--------|
| Positive control locus |  |  |
| Negative control locus |  |  |
| IgG control |  |  |
| No-antibody control |  |  |
| Input |  |  |

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
> Reviewer: check that every control row (positive/negative locus, IgG, no-antibody, input) is filled.

## Amendments

%% After sign-off, add corrections only here, one per line: - YYYY-MM-DD — Name — what changed and why %%
