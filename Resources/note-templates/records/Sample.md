<%*
/* TEMPLATE-INFO
template_id: TPL-R-SAMPLE
name: Sample
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
type: sample
id: <% id %>
title: "<% title %>"
description:
tags:
  - sample
created: <% today %>
updated: <% today %>
status: active
owner: <% settings.owner || "" %>
sample_code: <% title %>
sample_type:
source_kind:
organism:
tissue:
collection_date: <% today %>
collected_by: <% settings.owner || "" %>
storage_location:
quantity:
parent_sample:
projects: <% projects %>
human_or_community_data: false
ethics_approval:
consent_scope:
permitted_uses:
data_steward:
community_source:
benefit_sharing:
sharing_restrictions:
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
template_id: TPL-R-SAMPLE
template_version: 1.1.0
---
# <% title %>

> [!info] Sample `<% id %>`
> One note per physical sample or derived aliquot. Use **de-identified codes only** — never
> patient names, hospital/UHID numbers, phone numbers or dates of birth.
> `source_kind`: human · animal · cell_line · other. For human material set
> `human_or_community_data: true` and fill the CARE fields ([[CARE guide]]).
> Ontology ids: organism `NCBITaxon:9606` (human), tissue UBERON id where useful.

## Description

## Collection and processing

## Storage and chain of custody

| Date | From | To / location | Note |
|------|------|---------------|------|
|      |      |               |      |

## Derived samples

Derived aliquots (DNA, RNA, lysate…) are their own sample notes with `parent_sample` linking here.

## Used in

Experiments that link this sample appear in the backlinks pane.
