<%*
/* TEMPLATE-INFO
template_id: TPL-R-PROTOCOL
name: Protocol version
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
type: protocol
id: <% id %>
title: "<% title %>"
description:
tags:
  - protocol
created: <% today %>
updated: <% today %>
status: draft
owner: <% settings.owner || "" %>
protocol_family: <% ctx.protocol_family || title %>
version: <% ctx.version || "1.0.0" %>
supersedes: <% supersedes %>
biosafety_level: BSL-1
ibsc_approval:
source:
projects: []
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
template_id: TPL-R-PROTOCOL
template_version: 1.1.0
---
# <% title %>

> [!info] Protocol version `<% id %>`
> One note per **version**. Status: draft → validated → active → superseded / retired. Only
> `active` versions may be cited by new experiments. Never edit an active version that a
> completed experiment cites — create a new version with *New record → protocol version*, then
> set the old one to `superseded`.

## Purpose and scope

## Safety

- Biosafety level: `biosafety_level`; IBSC approval when BSL-2 or above / recombinant DNA.
- Hazards and PPE:
- Waste disposal:

## Materials and equipment

| Item | Identifier / catalogue no. | Amount | Note |
|------|----------------------------|--------|------|
|      |                            |        |      |

## Procedure

1.

## Expected results and QC criteria

## Troubleshooting

## References

Source protocol (DOI / protocols.io) in `source`.

## Version history

What changed compared with the version in `supersedes`:
