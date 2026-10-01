<%*
/* TEMPLATE-INFO
template_id: TPL-R-CODE
name: Code reference
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
type: code_ref
id: <% id %>
title: "<% title %>"
description:
tags:
  - code-ref
created: <% today %>
updated: <% today %>
status: active
owner: <% settings.owner || "" %>
repository:
commit:
version_tag:
environment:
entry_point:
language:
projects: <% projects %>
confidentiality: <% settings.default_confidentiality || "internal" %>
license: <% settings.default_license || "lab-internal" %>
ai_assisted: false
ai_note:
template_id: TPL-R-CODE
template_version: 1.1.0
---
# <% title %>

> [!info] Code reference `<% id %>`
> Analysis code, pipelines and notebooks stay in their repository; this note pins the exact
> version used. Required: `repository`, `commit` **or** `version_tag`, `entry_point`.

## What the code does

## How to run

- Environment (`environment`): e.g. `environment.yml`, `renv.lock`, container image
- Entry point (`entry_point`): notebook or script to start from
- Get the commit: `git rev-parse HEAD` in the repository

## Outputs

Link the DATA- references the code produced.
