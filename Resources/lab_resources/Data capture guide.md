---
type: guide
id: data-capture-guide
title: "Data capture guide"
description: "Where files and data go: small files in the vault, large or raw data by reference."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

# Data capture guide

Where every file of your research goes, so that anyone (including you in three years) can find
it, check it and reuse it. Part of the [[FAIR guide]].

## 1. In the vault or by reference?

| The file is… | Where it goes | How you record it |
|--------------|---------------|-------------------|
| Small (≤ 10 MB) **and** an open format — PNG/JPG/SVG image, PDF, CSV/TSV, TXT, JSON, rendered HTML report | `files/` inside the vault | Embed or link it in the experiment note |
| Large (> 10 MB) **or** raw instrument output — FASTQ/BAM/CRAM/VCF, `.czi`/`.lif`/`.nd2`/TIFF stacks, `.fcs`, mass-spec `.raw`/`.mzML`, `.h5ad`, model weights | Lab server / NAS / public archive — **never** the vault | A **data reference** note (`DATA-…`) via *New record → data reference*, linked in the experiment's `data_refs` |
| Code: analysis scripts, pipelines, notebooks (Jupyter, R Markdown, Quarto) | A Git repository (GitHub/GitLab, institutional server) | A **code reference** note (`CODE-…`) with the exact commit or tag, linked in `code_refs` |
| Anything with patient names, hospital/UHID numbers, phone numbers, dates of birth | **Nowhere in the vault** | Use de-identified sample codes only — see [[CARE guide]] |

The 10 MB limit is set in [[Vault settings]] (`max_attachment_mb`). The validator and *Vault
Health* flag files that are too big (AT001) or in raw formats (AT002). The vault's `.gitignore`
also blocks common raw-data extensions as a safety net.

## 2. Naming files in `files/`

```text
<ID>_<short-description>_<YYYYMMDD>.<ext>
EXP-PC-20261001-01_p53-blot_20261001.png
EXP-PC-20261001-01_plate-reader_20261002.csv
```

- Start with the record ID so every file sorts next to its siblings and is findable from the ID.
- Use hyphens inside the description, no spaces.
- Pasting an image creates `Pasted image ….png`; rename it straight away (right-click → *Rename*).
  Obsidian updates every link automatically. Until then the validator warns (AT003).

## 3. Originals vs figures

A cropped, annotated blot or a pretty plot in `files/` is a **derived** file. Its original
(uncropped scan, raw microscope image, instrument export) must stay findable:

1. Keep the original in lab storage, unmodified.
2. Register it as a data reference (`DATA-…`) with location and checksum.
3. In the experiment's *Results*, write under the embedded image: `Original: [[DATA-…]]`.

Journals and reviewers increasingly ask for uncropped originals — this makes that a 1-minute job.

## 4. Data references: what to fill

| Property | Example | Why |
|----------|---------|-----|
| `description` | Bulk RNA-seq FASTQ, 12 samples, batch 3 | What it is |
| `location` | `//labserver/seq/2026/run_0312/` or a URL | Where it is |
| `persistent_id` | `PRJNA123456`, `EGAS00001000000`, `10.5281/zenodo.123` | Stable identifier once deposited |
| `format` | FASTQ (gzip) | How to read it |
| `size` / `file_count` | 42 GB / 24 | What to expect when copying |
| `checksum` | `sha256:…` or path to `checksums.sha256` | Proves the files are unchanged |
| `steward` | Your name | Who answers questions |
| `access_conditions` | Lab members on request; controlled access via EGA | Who may use it |
| `license` | `lab-internal`, later `CC-BY-4.0` | Reuse terms |

Checksums: Windows `certutil -hashfile <file> SHA256`; macOS/Linux `sha256sum <file>`; for a
folder, write a manifest (`sha256sum * > checksums.sha256`) and put its path in `checksum`.

**Recommended repositories when you publish**: SRA/ENA (sequencing), **EGA** (controlled-access
human genomic data), GEO (expression), PRIDE (proteomics), BioImage Archive / IDR (images),
Zenodo (anything else, gives a DOI), GitHub/GitLab + Zenodo release (code).

## 5. Code references

Pin the **exact** version: `commit` (from `git rev-parse HEAD`) or a `version_tag`, the
`entry_point` (which notebook/script to run) and the `environment` (`environment.yml`,
`renv.lock`, container image). A notebook without its environment file is rarely reproducible.

## 6. Backups (3-2-1)

Keep **3** copies of important data on **2** different media, **1** off-site (e.g. lab server +
external drive + institutional cloud). Your vault itself is backed up by your private Git
repository; raw data are backed up by the lab's storage plan — ask your PI where that is
documented. Test restoring a file at least once a year.
