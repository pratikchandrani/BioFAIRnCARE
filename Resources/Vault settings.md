---
type: settings
id: vault-settings
title: "Vault settings"
description: "Your name, initials, PI and default properties used by every new note."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Vault Owner
owner_initials:
pi: Pratik Chandrani
lab: PC Lab
default_confidentiality: internal
default_license: lab-internal
vault_version: 2.0.0
max_attachment_mb: 10
edition: standard
confidentiality: internal
license: lab-internal
ai_assisted: false
---

# Vault settings

**Fill this in on your first day** — the *New experiment* and *New record* commands read it.

| Property | What to enter |
|----------|---------------|
| `owner` | Your full name, exactly as in [[Lab members]] (replace the placeholder "Vault Owner") |
| `owner_initials` | Your initials from [[Lab members]] (2–4 uppercase letters). Ask the maintainer to add you if you are not listed. |
| `pi` | Your PI or mentor (reviews and signs off your experiments) |
| `lab` | Lab name |
| `default_confidentiality` | `internal` (default), `confidential`, `embargoed` or `public` |
| `default_license` | `lab-internal` until data are published; then an SPDX id such as `CC-BY-4.0` |
| `vault_version` | BioFAIRnCARE release you installed (updated when you apply an update package) |
| `edition` | Set by the lab release (`standard` or `lite`) — do not change |
| `max_attachment_mb` | Largest file allowed inside the vault (default 10 MB); larger files are registered as data references |

This note belongs to you: lab update packages never overwrite it.
