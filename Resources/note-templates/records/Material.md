<%*
/* TEMPLATE-INFO
template_id: TPL-R-MATERIAL
name: Material
category: Records
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
| 1.1.0   | 2026-10-02 | Pratik Chandrani | Add OKF fields title, description and tags |
END TEMPLATE-INFO */
const settingsFile = app.vault.getAbstractFileByPath("Resources/Vault settings.md");
const settings = (settingsFile && app.metadataCache.getFileCache(settingsFile)?.frontmatter) || {};
const ctx = window.labvaultContext || {};
const today = tp.date.now("YYYY-MM-DD");
const m = tp.file.title.match(/^((?:PRT|SMP|MAT|INS|DATA|CODE|EVT)-[A-Z]{2,4}-\d{8}-\d{2})\s*(.*)$/);
const id = m ? m[1] : tp.file.title;
const title = (m ? m[2] : tp.file.title).replace(/"/g, "'");
const yamlList = (items) => (items && items.length) ? "\n" + items.map(l => '  - "' + l + '"').join("\n") : "[]";
const projects = yamlList((ctx.projects || []).map(p => String(p).startsWith("[[") ? p : "[[" + p + "]]"));
const supersedes = ctx.supersedes ? '"[[' + ctx.supersedes + ']]"' : "";
-%>
---
type: material
id: <% id %>
title: "<% title %>"
description:
tags:
  - material
created: <% today %>
updated: <% today %>
status: active
owner: <% settings.owner || "" %>
material_kind:
supplier:
catalog_no:
lot_no:
rrid:
identifier:
storage:
qc_status:
str_authenticated_on:
mycoplasma_tested_on:
passage_at_receipt:
projects: []
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
template_id: TPL-R-MATERIAL
template_version: 1.1.0
---
# <% title %>

> [!info] Material `<% id %>`
> `material_kind`: cell_line · antibody · reagent · kit · plasmid · primer · organism_strain.
> Give the persistent identifier where one exists: **RRID** for antibodies and cell lines
> (Cellosaurus `CVCL_…`), Addgene id for plasmids, ChEBI/PubChem for chemicals, NCBI Taxonomy for
> strains. Record a new lot as a new note (or a new row below) so experiments cite the exact lot.

## Details

## Lots

| Lot no. | Received | Expiry | Opened | Note |
|---------|----------|--------|--------|------|
|         |          |        |        |      |

## Quality control

Cell lines: STR authentication (`str_authenticated_on`) and mycoplasma test
(`mycoplasma_tested_on`) — see template A2.

## Used in

Experiments that link this material appear in the backlinks pane.
