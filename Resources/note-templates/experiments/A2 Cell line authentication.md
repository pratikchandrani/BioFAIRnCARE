<%*
/* TEMPLATE-INFO
template_id: TPL-A2
name: Cell line receipt, authentication & mycoplasma testing
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
-%>
---
type: experiment
id: <% id %>
title: "<% title %>"
description:
tags:
  - experiment
  - biospecimens-materials
experiment_type: A2
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
biosafety_level: BSL-1
ibsc_approval:
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
review_requested: false
signed_off_by:
signed_off_on:
template_id: TPL-A2
template_version: 1.1.0
---
# <% title %>

%% description (in Properties): one sentence — what you did and why; add the result when finished. %%

> [!info] Cell line receipt, authentication & mycoplasma testing · `<% id %>`
> Register a new cell line and confirm identity (STR) and mycoplasma status before use.
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

## Identity

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Source / RRID (Cellosaurus) |  |  | e.g. CVCL_0023 |
| Supplier and lot |  |  |  |
| Passage at receipt |  |  |  |
| STR method / provider |  |  |  |
| STR match to reference |  |  | % (≥ 80 % = match) |
| Master / working bank vials frozen |  |  | number, location |

## Mycoplasma test

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Kit / method (lot) |  |  |  |
| Cells cultured without antibiotic for |  |  | days |
| Confluency at sampling |  |  | % |
| Sample collected (supernatant / cells) |  |  |  |
| PCR set-up |  |  |  |
| Total reaction volume |  |  | µL |
| Result |  |  | negative / positive |

Run the gel with template **B8 Agarose gel** and link that experiment here, or fill the map below.

| Lane | Sample (ID or link) | Type | Amount loaded | Primer pair / probe | Expected size (bp) | Band observed |
|------|---------------------|------|---------------|---------------------|--------------------|---------------|
| 1 | Ladder |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 | Negative control |  |  |  |  |  |
| 5 | Positive control |  |  |  |  |  |
| 6 | NTC (no-template control) |  |  |  |  |  |

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
