---
type: experiment
id: EXP-EX-20260115-01
description: "Western blot detecting p53 (beta-actin control) in A549 lysates before TP53 knockdown; transfer extended to 75 min."
tags:
  - experiment
  - proteins
title: p53 western blot
created: 2026-01-15
updated: 2026-01-15
experiment_type: C2
start_date: 2026-01-15
end_date: 2026-01-15
status: completed
owner: Example Student
contributors: []
projects:
  - "[[DemoTP53Project]]"
protocols:
  - "[[PRT-EX-20260110-01 Western blot v1.0.0]]"
samples: []
materials:
  - "[[MAT-EX-20260105-01 A549 cell line]]"
  - "[[MAT-EX-20260105-02 Anti-p53 antibody]]"
instruments:
  - "[[INS-EX-20260105-01 Gel imager]]"
data_refs:
  - "[[DATA-EX-20260115-01 Uncropped blot scans]]"
code_refs: []
outcome: success
outcome_reason:
literature: []
human_or_community_data: false
animal_study: false
confidentiality: internal
license: lab-internal
ai_assisted: false
ai_note:
review_requested: false
signed_off_by:
signed_off_on:
example: true
template_id: TPL-C2
template_version: 1.0.0
---
> [!example] Fictional example — all names, numbers and locations are made up.

# p53 western blot

## Aim / hypothesis
Confirm p53 protein in A549 lysates before knockdown.

## Materials

| Material | Identifier (RRID / ontology / Addgene) | Supplier | Catalogue no. | Lot no. | Note |
|----------|----------------------------------------|----------|---------------|---------|------|
| [[MAT-EX-20260105-02 Anti-p53 antibody]] | AB_EXAMPLE53 (fictional) | Example Biotech | EX-AB-53 | EX-LOT-7781 | 1:1000 |

## Protocol and deviations
- Protocol: [[PRT-EX-20260110-01 Western blot v1.0.0]]
- Deviation: transfer 75 min instead of 60 min (thicker gel).

## Transfer

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Membrane | PVDF | | |
| Transfer buffer | Tris-glycine + 20 % methanol | | |
| Method | wet | | |
| Conditions | 100 V, 75 min, 4 °C | | deviation from protocol (60 min) |
| Ponceau S verification | even transfer across all lanes | OK | image kept with the raw scans |

## Primary antibodies

| Target | Antibody (material record / RRID) | Host | Dilution | Incubation |
|--------|-----------------------------------|------|----------|------------|
| Target protein | [[MAT-EX-20260105-02 Anti-p53 antibody]] (AB_EXAMPLE53, fictional) | mouse | 1:1000 | overnight, 4 °C |
| Housekeeping protein | anti-β-actin (fictional lot EX-LOT-0901) | rabbit | 1:5000 | 1 h, RT |

## Detection

| Step | Parameter / setting | Value | Note |
|------|---------------------|-------|------|
| Detection method | ECL | | |
| Imaging system | [[INS-EX-20260105-01 Gel imager]] | | |
| Exposure | | 5 s and 30 s | auto-exposure first |
| Image files | | | preview in files/; raw scans in [[DATA-EX-20260115-01 Uncropped blot scans]] |

## Quantification

| Lane | Sample | Target intensity | Housekeeping intensity | Normalised ratio |
|------|--------|------------------|------------------------|------------------|
| 2 | A549 untreated | 15 200 | 30 100 | 1.00 |
| 3 | A549 + cisplatin 10 µM | 28 900 | 29 600 | 1.93 |

**Normalised ratio** = 1.93  — formula: target ÷ housekeeping, then ÷ the control lane's ratio

- Software and version: Fiji 2.14 (fictional analysis)

## Results

### Files in the vault

![[EXP-EX-20260115-01_p53-blot_20260115.png]]

Original: [[DATA-EX-20260115-01 Uncropped blot scans]]

## Progress log

- [[_Examples/daily_notes/2026-01-15|2026-01-15]] — created

## Sign-off

Not yet reviewed (examples are never signed off).

## Amendments
