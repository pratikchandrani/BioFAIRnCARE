---
type: settings
id: lab-members
title: "Lab members"
description: "Lab members with their initials and roles, used for record IDs."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: internal
license: lab-internal
ai_assisted: false
lab_owned: true
---

# Lab members

Lab-wide list of people who keep a vault, the **initials** used in their record IDs
(`EXP-<INITIALS>-YYYYMMDD-NN`), and who may **sign off** experiments.

- Maintained by the vault maintainer (PI or delegate). Students do not edit this note: every lab
  update replaces it.
- Initials are 2–4 uppercase letters and must be unique in the lab. If two people share initials,
  the maintainer assigns a longer form (e.g. `PC` and `PCH`).
- **Reviewers** (role `reviewer` or `pi`, status `active`) can sign off experiments. A sign-off is
  valid only when it is committed under the reviewer's own Git identity (the `Git email` column
  must match `git config user.email` on the reviewer's computer).
- People who leave are set to `inactive`, never deleted, so their past sign-offs stay valid.

## Members

| Name             | Initials | Role    | Git email                | Status |
| ---------------- | -------- | ------- | ------------------------ | ------ |
| Pratik Chandrani | PC       | pi      | something@gmail.com      | active |
| Isha Shinde      | IS       | student | someotherthing@gmail.com | active |

%% Replace the example e-mail addresses with each person's Git commit e-mail. The "Example Student"
row is used by the fictional notes in _Examples/; keep it while those examples exist. %%
