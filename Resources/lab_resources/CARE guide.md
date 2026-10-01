---
type: guide
id: care-guide
title: "CARE guide"
description: "How to record human, patient-derived and community data under the CARE principles."
created: 2026-10-01
updated: 2026-10-02
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

# CARE guide — people and communities behind the data

The CARE Principles for Indigenous Data Governance — **Collective benefit, Authority to control,
Responsibility, Ethics** — were published by the Global Indigenous Data Alliance (Carroll et al.,
"The CARE Principles for Indigenous Data Governance", *Data Science Journal* 19:43, 2020,
https://doi.org/10.5334/dsj-2020-043). They complement FAIR: FAIR is about data, CARE is about
**people and purpose**.

CARE was written for Indigenous Peoples' data. This lab applies it **in full** to data from
Indigenous, tribal (Adivasi) and other distinct communities, and applies its spirit to all
data derived from patients and research participants: cancer research uses tissue, blood and
genomes donated by people who trust us with them.

## When CARE applies in this vault

Set `human_or_community_data: true` on a sample, experiment, data reference or project whenever
it involves human biospecimens, clinical or genomic data from people, or data about a community.
The validator and *Vault Health* then require the CARE fields (rule CA001):

| Property | Write here | CARE |
|----------|------------|------|
| `ethics_approval` | IEC/IRB approval reference (and IBSC if relevant) | E, A |
| `consent_scope` | What participants agreed to (e.g. "research on lung cancer, genomic data, future use in cancer research") | A1 |
| `permitted_uses` | Uses that are allowed — and not allowed (e.g. no commercial use) | A3, E3 |
| `data_steward` | The person/office accountable for the data and contactable about it | R1, A3 |
| `community_source` | De-identified description of where the material comes from (hospital, cohort, community) and any cultural sensitivities | C, A1, R3 |
| `benefit_sharing` | How results or benefits return (return of actionable findings via clinicians, reports to the community, capacity building) | C3, E2 |
| `sharing_restrictions` | Conditions for any onward sharing (controlled access, data-access committee, no re-identification) | A3, E3 |

## The 12 CARE principles in a cancer-research lab

| # | Principle | What it means here | Vault support |
|---|-----------|--------------------|---------------|
| C1 | For inclusive development and innovation | Research should be able to benefit the communities and patients whose data it uses | `community_source`; project aims that state who benefits |
| C2 | For improved governance and citizen engagement | Data should help communities and patients understand and take part in decisions | `data_steward` as a contact point; plain-language summaries in project notes |
| C3 | For equitable outcomes | Benefits (knowledge, diagnostics, care) are shared fairly | `benefit_sharing` |
| A1 | Recognising rights and interests | People and communities have rights over data about them; consent defines what we may do | `consent_scope`; de-identified codes only — names, UHID/hospital numbers, phone numbers or dates of birth never enter the vault (rule PV001) |
| A2 | Data for governance | Communities should be able to access data about them for their own governance | `steward` / `data_steward` and `access_conditions` say how access is requested |
| A3 | Governance of data | Rules for use and sharing are set with — not only for — the people concerned | `permitted_uses`, `sharing_restrictions`, `access_conditions`; controlled-access repositories (EGA) |
| R1 | For positive relationships | Work built on trust, respect and reciprocity with participants, clinicians and communities | Named `data_steward`; record agreements in the project |
| R2 | For expanding capability and capacity | Research should build skills and data capacity, including in the communities involved | Onboarding guides and worked examples; note training/outreach in projects |
| R3 | For Indigenous languages and worldviews | Respect cultural context, language and worldviews in how data are described and used | Record sensitivities in `community_source`; avoid stigmatising labels |
| E1 | For minimising harm and maximising benefit | Avoid harm (re-identification, stigma, discrimination) | Privacy rule PV001, `confidentiality`, private repositories, no identifiers in notes |
| E2 | For justice | Address power imbalances; fair distribution of burdens and benefits | Ethics approval required; `benefit_sharing` |
| E3 | For future use | Future and secondary uses stay within what was agreed | `permitted_uses` and `sharing_restrictions` stay attached to data references |

## Practical rules

- **Never** write names, initials of participants, hospital/UHID/MRN numbers, phone numbers,
  addresses, Aadhaar/PAN or dates of birth in any note. Use the biobank's de-identified code.
  The key linking codes to people stays with the hospital/biobank, outside the vault.
- If the validator flags a number that is genuinely not about a person (e.g. a lab landline),
  confirm and add `%% pv-allow: reason %%` on that line.
- Before depositing human genomic data publicly, check the consent: most patient genomes belong in
  a **controlled-access** archive (e.g. EGA), not an open one.
- Do not send identifiable or unpublished participant data to external AI tools (constitution,
  Principle VII). Mark AI-assisted text with `ai_assisted: true` and `ai_note`.
- Animal work is covered separately: IAEC approval, humane end-points and a 3Rs statement are
  required in templates E1/E2 (rule AN001).

## How this relates to OKF

The lab can export curated knowledge in the **Open Knowledge Format** (OKF) for other tools or
AI agents ([[OKF guide]]). CARE comes first: every note with `human_or_community_data: true` is
**left out** of such exports by default. Only the **PI** may set `okf_export: allowed` on that
note, after checking its `ethics_approval`, `consent_scope`, `permitted_uses` and
`sharing_restrictions`. The setting never overrides `confidential` or `embargoed` — those notes
always stay in the lab. Students never set `okf_export` themselves.
