<%*
/* TEMPLATE-INFO
template_id: TPL-CMD-NEW-EXPERIMENT
name: New experiment (command)
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
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Pick a catalogue template, create <Title>_<INI>-<YYYYMMDD>-<NN> in Experiments/, add "- Performed [[…]]" to the daily note |
END TEMPLATE-INFO */
// Run from today's daily note (button, Ctrl/Cmd+Alt+E or command palette). The experiment is always a
// separate note; the daily note only receives one log line. Behaviour: contracts/command-behaviour.md (spec 003).
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const lv = await new AsyncFunction("app", "tp", await app.vault.adapter.read("Resources/lab_resources/scripts/labvault-commands.js"))(app, tp);

const ini = lv.initials();
if (!ini) return;

const schema = JSON.parse(await app.vault.adapter.read("Resources/lab_resources/schema/note-types.json"));
const templates = await lv.listTemplates("experiments");
const options = [];
for (const entry of schema.catalogue) {
  const t = templates[entry.template_id];
  if (!t) continue;
  const label = `${entry.code} · ${entry.name}` + (t.local ? `  (your local copy ${t.info.version})` : `  v${t.info.version}`);
  options.push({ label, entry, file: t.file });
}
const choice = await tp.system.suggester(options.map(o => o.label), options, false, "Experiment type (type to filter, e.g. 'pcr')");
if (!choice) return;

const title = lv.sanitize(await tp.system.prompt("Short title (e.g. PCR of breast cancer tissues)", "", false));
if (!title) { new Notice("No title given — nothing created."); return; }

const target = await lv.targetDaily();
const ymd = window.moment().format("YYYYMMDD");
const next = lv.nextId("EXP", ini, ymd);
if (!next) return;
const fileName = `${title}_${ini}-${ymd}-${next.nn}`;
const folder = target.example ? "_Examples/Experiments" : "Experiments";
if (!app.vault.getAbstractFileByPath(folder)) await app.vault.createFolder(folder);

const dailyFm = lv.fmOf(target.file);
window.labvaultContext = {
  id: next.id,
  title,
  start_date: target.date,
  projects: Array.isArray(dailyFm.projects) ? dailyFm.projects : (dailyFm.projects ? [dailyFm.projects] : []),
  origin: target.file.basename,
};
let created;
try {
  created = await tp.file.create_new(choice.file, fileName, false, folder);
} finally {
  delete window.labvaultContext;
}
if (!created) { new Notice("Could not create the experiment note."); return; }

await lv.insertLogLine(target, `- Performed [[${fileName}]]`);
await app.workspace.getLeaf("tab").openFile(created);
new Notice(`Created ${fileName} (${choice.entry.name})`);
-%>
