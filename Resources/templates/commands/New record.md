<%*
/* TEMPLATE-INFO
template_id: TPL-CMD-NEW-RECORD
name: New record (command)
category: Command
version: 1.0.0
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
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Create sample, material, instrument, protocol version, data/code reference, project, concept, literature or event notes with IDs |
END TEMPLATE-INFO */
// Run from a daily note (button, Ctrl/Cmd+Alt+R or command palette). The record is a separate note in
// its folder; the daily note gets "- Registered [[…]]". Behaviour: contracts/command-behaviour.md (spec 003).
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const lv = await new AsyncFunction("app", "tp", await app.vault.adapter.read("Resources/lab_resources/scripts/labvault-commands.js"))(app, tp);

const TYPES = [
  { label: "🧫 Sample (de-identified)", tpl: "TPL-R-SAMPLE", prefix: "SMP", folder: "Samples", ask: "Sample code (de-identified, e.g. LUAD-T-014)" },
  { label: "🧴 Material (cell line, antibody, reagent, kit, plasmid, primer, strain)", tpl: "TPL-R-MATERIAL", prefix: "MAT", folder: "Materials", ask: "Material name (e.g. Anti-p53 DO-1)" },
  { label: "🔬 Instrument", tpl: "TPL-R-INSTRUMENT", prefix: "INS", folder: "Materials", ask: "Instrument name (e.g. ChemiDoc MP)" },
  { label: "📋 Protocol version", tpl: "TPL-R-PROTOCOL", prefix: "PRT", folder: "Protocols", protocol: true },
  { label: "💾 Data reference (large / raw data kept outside the vault)", tpl: "TPL-R-DATA", prefix: "DATA", folder: "Data", ask: "Short description (e.g. RNA-seq FASTQ batch 3)" },
  { label: "🧑‍💻 Code reference (repository / notebook)", tpl: "TPL-R-CODE", prefix: "CODE", folder: "Data", ask: "Repository or notebook name" },
  { label: "🎯 Project", tpl: "TPL-R-PROJECT", folder: "Projects/Auto_summary", slug: true, ask: "Project tag name, no spaces (e.g. TP53Cisplatin)" },
  { label: "💡 Concept", tpl: "TPL-R-CONCEPT", folder: "Concepts", ask: "Concept name (e.g. Apoptosis)" },
  { label: "📚 Literature note", tpl: "TPL-R-LITERATURE", folder: "Zotero_PDF_notes", ask: "Citekey (e.g. SmithTP532024)", slug: true },
  { label: "📅 Event (journal club, WoW, talk, conference, lab meeting)", tpl: "TPL-R-EVENT", prefix: "EVT", folder: "Events", ask: "Event title" },
];

const kind = await tp.system.suggester(TYPES.map(t => t.label), TYPES, false, "What kind of record?");
if (!kind) return;
const templates = await lv.listTemplates("records");
const tplEntry = templates[kind.tpl];
if (!tplEntry) { new Notice(`Template ${kind.tpl} not found in Resources/note-templates/records/.`); return; }

const ctx = {};
let name;
if (kind.protocol) {
  const protocols = app.vault.getMarkdownFiles().filter(f => lv.fmOf(f).type === "protocol").sort((a, b) => b.basename.localeCompare(a.basename));
  const modes = ["New protocol (version 1.0.0)", ...protocols.map(f => `New version of: ${f.basename}  [${lv.fmOf(f).status}]`)];
  const pick = await tp.system.suggester(modes, ["new", ...protocols], false, "New protocol or new version of an existing one?");
  if (!pick) return;
  if (pick !== "new") {
    const old = lv.fmOf(pick);
    const parts = String(old.version || "1.0.0").split(".").map(n => parseInt(n, 10) || 0);
    const version = lv.sanitize(await tp.system.prompt("New version number (MAJOR.MINOR.PATCH)", `${parts[0]}.${(parts[1] || 0) + 1}.0`, false), 20);
    if (!/^\d+\.\d+\.\d+$/.test(version)) { new Notice("Version must look like 1.2.0"); return; }
    ctx.protocol_family = old.protocol_family || pick.basename;
    ctx.version = version;
    ctx.supersedes = pick.basename;
  } else {
    ctx.protocol_family = lv.sanitize(await tp.system.prompt("Protocol name (e.g. Western blot)", "", false));
    if (!ctx.protocol_family) return;
    ctx.version = "1.0.0";
  }
  name = `${ctx.protocol_family} v${ctx.version}`;
} else {
  name = lv.sanitize(await tp.system.prompt(kind.ask, "", false));
  if (kind.slug) name = name.replace(/\s+/g, "");
  if (!name) { new Notice("Nothing entered — no record created."); return; }
}

let fileName = name;
if (kind.prefix) {
  const ini = lv.initials();
  if (!ini) return;
  const next = lv.nextId(kind.prefix, ini, window.moment().format("YYYYMMDD"));
  if (!next) return;
  fileName = `${next.id} ${name}`;
}

const target = await lv.targetDaily();
const dailyFm = lv.fmOf(target.file);
ctx.projects = Array.isArray(dailyFm.projects) ? dailyFm.projects : (dailyFm.projects ? [dailyFm.projects] : []);
const folder = (target.example ? "_Examples/" : "") + kind.folder;
if (!app.vault.getAbstractFileByPath(folder)) await app.vault.createFolder(folder);
if (app.vault.getAbstractFileByPath(`${folder}/${fileName}.md`)) {
  new Notice(`${fileName} already exists — linking it.`);
  await lv.insertLogLine(target, `- Registered [[${fileName}]]`);
  return;
}
window.labvaultContext = ctx;
let created;
try {
  created = await tp.file.create_new(tplEntry.file, fileName, false, folder);
} finally {
  delete window.labvaultContext;
}
if (!created) { new Notice("Could not create the record."); return; }
await lv.insertLogLine(target, `- Registered [[${fileName}]]`);
await app.workspace.getLeaf("tab").openFile(created);
-%>
