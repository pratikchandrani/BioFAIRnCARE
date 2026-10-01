<%*
/* TEMPLATE-INFO
template_id: TPL-E2
name: Xenograft drug sensitivity / efficacy
category: E. In vivo
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
  - in-vivo
experiment_type: E2
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
animal_study: true
ethics_approval:
consent_scope:
permitted_uses:
data_steward:
community_source:
benefit_sharing:
sharing_restrictions:
iaec_approval:
humane_endpoints:
three_rs:
species_strain:
animal_count:
biosafety_level: BSL-2
ibsc_approval:
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
review_requested: false
signed_off_by:
signed_off_on:
template_id: TPL-E2
template_version: 1.1.0
---
# <% title %>

%% description (in Properties): one sentence — what you did and why; add the result when finished. %%

> [!info] Xenograft drug sensitivity / efficacy · `<% id %>`
> Test a treatment's effect on established xenografts (ARRIVE-aligned).
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

## Type-specific parameters

| Parameter | Value | Unit / note |
|-----------|-------|-------------|
| Groups and n per group |  |  |
| Randomisation method |  |  |
| Blinding |  |  |
| Treatment start criterion |  | tumour volume mm³ |
| Compound, dose, route, schedule |  |  |
| Vehicle control |  |  |
| Body weight monitoring |  |  |
| Tumour volume measurements |  | `files/…csv` |
| Tumour growth inhibition (TGI) |  | % |
| Statistical analysis |  |  |
| End-points reached |  |  |

## Human / community-derived material (CARE)

If any material or data comes from people or a community, set `human_or_community_data: true`
and fill: `ethics_approval` (IEC/IRB ref), `consent_scope`, `permitted_uses`, `data_steward`,
`community_source` (de-identified description), `benefit_sharing` (return of results / benefit
commitments), `sharing_restrictions`. See [[CARE guide]].

## Animal ethics

Required before any animal work: `iaec_approval` (IAEC protocol number), `humane_endpoints`
(criteria for ending the study for an animal, e.g. tumour > 1500 mm³ or > 20 % weight loss),
`three_rs` (replacement / reduction / refinement statement), `species_strain` (with NCBI Taxonomy
id, e.g. NCBITaxon:10090 NOD-scid IL2Rγnull), `animal_count`. Report following ARRIVE 2.0.

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
