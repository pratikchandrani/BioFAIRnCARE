---
type: index
id: experiment-catalogue
title: "Experiment catalogue"
description: "Every experiment template in the vault, with its purpose, extra fields and live version."
created: 2026-10-01
updated: 2026-10-01
status: active
owner: Lab
confidentiality: public
license: CC-BY-4.0
ai_assisted: false
lab_owned: true
---

# Experiment catalogue

Every experiment template in the vault. Start one from your daily note with **New experiment**
(`Ctrl/Cmd+Alt+E`): it creates `Experiments/<Title>_<INI>-<YYYYMMDD>-<NN>.md` and adds
`- Performed [[…]]` to the daily note — you never copy templates by hand. All templates share the same FAIR core
(aim, materials with lot numbers, protocol version, procedure, results, data/code references,
progress log, amendments) and add a **type-specific parameters** table.

Need a template that is missing? Use **Z1 Generic experiment** now and ask the vault maintainer;
new templates arrive with the next lab update. To adapt a template to your own work, run
**Customise template** (your copy lives in `Resources/note-templates/local/`; see [[Template register]]).

| Code | Category | Template | Use it for | Extra fields | File |
|------|----------|----------|------------|--------------|------|
| A1 | A. Biospecimens & materials | Clinical sample collection & biobanking | Collect, process and bank de-identified patient tissue, blood or body fluids. | CARE required, biosafety | [[Resources/note-templates/experiments/A1 Clinical sample collection\|template]] |
| A2 | A. Biospecimens & materials | Cell line receipt, authentication & mycoplasma testing | Register a new cell line and confirm identity (STR) and mycoplasma status before use. | biosafety | [[Resources/note-templates/experiments/A2 Cell line authentication\|template]] |
| A3 | A. Biospecimens & materials | Cell culture maintenance, passaging & cryopreservation | Routine culture, passaging and freezing of a cell line. | biosafety | [[Resources/note-templates/experiments/A3 Cell culture maintenance\|template]] |
| B1 | B. Nucleic acids | DNA / RNA extraction & QC | Extract nucleic acids and record yield, purity and integrity. | CARE if human data | [[Resources/note-templates/experiments/B1 DNA RNA extraction\|template]] |
| B2 | B. Nucleic acids | Conventional PCR & agarose gel electrophoresis | Amplify a target and check the product on an agarose gel. |  | [[Resources/note-templates/experiments/B2 PCR and gel\|template]] |
| B3 | B. Nucleic acids | cDNA synthesis & RT-qPCR | Measure gene expression by reverse transcription and quantitative PCR (MIQE-aligned). |  | [[Resources/note-templates/experiments/B3 RT-qPCR\|template]] |
| B4 | B. Nucleic acids | Gene cloning | Clone an insert into a vector and verify the construct. | biosafety | [[Resources/note-templates/experiments/B4 Gene cloning\|template]] |
| B5 | B. Nucleic acids | Plasmid preparation & transfection / viral transduction | Prepare plasmid DNA and deliver it (or virus) into cells. | biosafety | [[Resources/note-templates/experiments/B5 Plasmid prep and transfection\|template]] |
| B6 | B. Nucleic acids | Gene knockdown / knockout (siRNA, shRNA, CRISPR) | Reduce or remove a gene's expression and validate the effect. | biosafety | [[Resources/note-templates/experiments/B6 Knockdown knockout\|template]] |
| B7 | B. Nucleic acids | Chromatin immunoprecipitation (ChIP / ChIP-qPCR) | Map protein–DNA interactions at chosen loci by immunoprecipitating crosslinked chromatin. |  | [[Resources/note-templates/experiments/B7 ChIP\|template]] |
| B8 | B. Nucleic acids | Agarose gel electrophoresis | Separate and document nucleic acids on an agarose gel (stand-alone or after PCR, digests, ChIP). |  | [[Resources/note-templates/experiments/B8 Agarose gel\|template]] |
| C1 | C. Proteins | Protein extraction & quantification | Lyse cells or tissue and quantify protein. |  | [[Resources/note-templates/experiments/C1 Protein extraction\|template]] |
| C2 | C. Proteins | Western blot | Detect and compare proteins by SDS-PAGE and immunoblotting. |  | [[Resources/note-templates/experiments/C2 Western blot\|template]] |
| C3 | C. Proteins | Immunoprecipitation / Co-IP | Pull down a protein (and its partners) with an antibody. |  | [[Resources/note-templates/experiments/C3 Immunoprecipitation\|template]] |
| C4 | C. Proteins | ELISA | Quantify an analyte with an enzyme-linked immunosorbent assay. | CARE if human data | [[Resources/note-templates/experiments/C4 ELISA\|template]] |
| C5 | C. Proteins | Immunofluorescence / immunocytochemistry / immunohistochemistry | Localise proteins in cells or tissue sections. | CARE if human data | [[Resources/note-templates/experiments/C5 Immunostaining IF IHC\|template]] |
| C6 | C. Proteins | SDS-PAGE & total-protein staining | Separate proteins by SDS-PAGE and stain the gel (Coomassie / silver) without blotting. |  | [[Resources/note-templates/experiments/C6 SDS-PAGE and staining\|template]] |
| C7 | C. Proteins | Electrophoretic mobility shift assay (EMSA) | Detect protein–nucleic acid binding as a shift of a labelled probe on a native gel. |  | [[Resources/note-templates/experiments/C7 EMSA\|template]] |
| D1 | D. Cell-based assays | Cell proliferation / growth curve | Measure growth over time. |  | [[Resources/note-templates/experiments/D1 Cell proliferation\|template]] |
| D2 | D. Cell-based assays | Drug treatment & cytotoxicity (MTT / MTS / resazurin) | Determine dose-response and IC50 of a compound. |  | [[Resources/note-templates/experiments/D2 Drug cytotoxicity MTT\|template]] |
| D3 | D. Cell-based assays | Colony formation (clonogenic) assay | Assess long-term survival after treatment. |  | [[Resources/note-templates/experiments/D3 Colony formation\|template]] |
| D4 | D. Cell-based assays | Migration & invasion (wound healing / transwell) | Measure cell migration or invasion. |  | [[Resources/note-templates/experiments/D4 Migration invasion\|template]] |
| D5 | D. Cell-based assays | Flow cytometry (apoptosis, cell cycle, markers) | Analyse cells by flow cytometry. |  | [[Resources/note-templates/experiments/D5 Flow cytometry\|template]] |
| E1 | E. In vivo | Xenograft tumour formation (CDX / PDX) | Test tumour formation from implanted cells or patient tissue. | CARE if human data, animal ethics required, biosafety | [[Resources/note-templates/experiments/E1 Xenograft tumour formation\|template]] |
| E2 | E. In vivo | Xenograft drug sensitivity / efficacy | Test a treatment's effect on established xenografts (ARRIVE-aligned). | CARE if human data, animal ethics required, biosafety | [[Resources/note-templates/experiments/E2 Xenograft drug efficacy\|template]] |
| F1 | F. Omics | Whole exome sequencing | From sample to variant calls. | CARE if human data | [[Resources/note-templates/experiments/F1 Whole exome sequencing\|template]] |
| F2 | F. Omics | Transcriptome / RNA-seq | Bulk or single-cell transcriptome profiling. | CARE if human data | [[Resources/note-templates/experiments/F2 Transcriptome RNA-seq\|template]] |
| F3 | F. Omics | Microbiome (16S rRNA amplicon / shotgun metagenomics) | Profile microbial communities (MIxS-aligned). | CARE if human data | [[Resources/note-templates/experiments/F3 Microbiome\|template]] |
| G1 | G. Computational | Protein structure modelling, docking & molecular dynamics | Model a protein, dock ligands or run MD simulations. |  | [[Resources/note-templates/experiments/G1 Protein modelling and MD\|template]] |
| G2 | G. Computational | Machine-learning model training & evaluation | Train and evaluate a predictive model reproducibly. | CARE if human data | [[Resources/note-templates/experiments/G2 ML model training\|template]] |
| G3 | G. Computational | Exploratory data analysis (Jupyter / R Markdown / Quarto) | Explore a dataset in a notebook and record what was learned. | CARE if human data | [[Resources/note-templates/experiments/G3 Exploratory data analysis\|template]] |
| Z1 | Z. Fallback | Generic experiment | Any experiment not covered by a specific template (still fully FAIR). |  | [[Resources/note-templates/experiments/Z1 Generic experiment\|template]] |

## Live versions

```dataviewjs
const schema = JSON.parse(await app.vault.adapter.read("Resources/lab_resources/schema/note-types.json"));
const info = async (path) => {
  const text = await app.vault.adapter.read(path);
  const block = (text.split("/* TEMPLATE-INFO")[1] || "").split("CHANGELOG")[0];
  const o = {};
  for (const line of block.split("\n")) { const i = line.indexOf(":"); if (i > 0) o[line.slice(0, i).trim()] = line.slice(i + 1).trim(); }
  return o;
};
const rows = [];
for (const e of schema.catalogue) {
  const i = await info(e.file);
  rows.push([e.code, e.name, i.version, i.status]);
}
dv.table(["Code", "Template", "Version", "Status"], rows);
```

*This table is generated by `tools/scaffold_experiment_templates.py` in the stage area.*
