<%*
/* TEMPLATE-INFO
template_id: TPL-R-DATA
name: Data reference
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
type: data_ref
id: <% id %>
title: "<% title %>"
tags:
  - data-ref
created: <% today %>
updated: <% today %>
status: active
owner: <% settings.owner || "" %>
description:
location:
persistent_id:
format:
size:
file_count:
checksum:
access_conditions: Lab members on request
steward: <% settings.owner || "" %>
generated_on: <% today %>
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
template_id: TPL-R-DATA
template_version: 1.1.0
---
# <% title %>

> [!info] Data reference `<% id %>`
> Large or raw data **stay where they are** (lab server, NAS, public archive); this note makes them
> findable and reusable. Required: `location`, `format`, `size`, `checksum`, `steward`,
> `access_conditions`. See [[Data capture guide]].

## What the data are

## Location and identifiers

- Storage path / URL: `location`
- Persistent identifier / accession (SRA, ENA, EGA, GEO, PRIDE, Zenodo DOI): `persistent_id`

## Integrity

Record a checksum so anyone can verify the files later:

- Windows: `certutil -hashfile <file> SHA256`
- macOS / Linux: `sha256sum <file>` (for a folder: `sha256sum * > checksums.sha256` and put the
  manifest path in `checksum`)

Write it as `sha256:<64 hex characters>`.

## Access and reuse

Who may access, under which conditions (`access_conditions`, `license`). For human-derived data
set `human_or_community_data: true` and fill the CARE fields.

## Used by

Experiments that link this reference appear in the backlinks pane.
