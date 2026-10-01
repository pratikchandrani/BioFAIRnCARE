<%*
/* TEMPLATE-INFO
template_id: TPL-CMD-LOG-EXPERIMENT
name: Log to experiment (command)
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
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Add the daily note to an experiment's progress log and "- Continued [[…]]" to the daily note |
END TEMPLATE-INFO */
// Run from a daily note (button, Ctrl/Cmd+Alt+L or command palette). Behaviour: contracts/command-behaviour.md (spec 003).
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const lv = await new AsyncFunction("app", "tp", await app.vault.adapter.read("Resources/lab_resources/scripts/labvault-commands.js"))(app, tp);

const target = await lv.targetDaily();
const folder = target.example ? "_Examples/Experiments/" : "Experiments/";
const open = app.vault.getMarkdownFiles()
  .filter(f => f.path.startsWith(folder) && ["planned", "in-progress"].includes(lv.fmOf(f).status))
  .sort((a, b) => b.stat.mtime - a.stat.mtime);
if (!open.length) { new Notice("No planned or in-progress experiments. Use New experiment first."); return; }
const exp = await tp.system.suggester(open.map(f => `${f.basename}  [${lv.fmOf(f).status}]`), open, false, "Which experiment did you work on?");
if (!exp) return;

const day = target.file.basename;
const entry = `- [[${day}]] — `;
await app.vault.process(exp, (text) => {
  const lines = text.split("\n");
  const start = lines.findIndex(l => l.trim() === "## Progress log");
  if (start === -1) return text.trimEnd() + "\n\n## Progress log\n\n" + entry + "\n";
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) { if (/^#{1,6}\s/.test(lines[i])) { end = i; break; } }
  if (lines.slice(start, end).some(l => l.trim().startsWith(`- [[${day}]]`))) return text;
  let insertAt = start + 1;
  for (let i = start + 1; i < end; i++) { if (lines[i].trim().startsWith("- ")) insertAt = i + 1; }
  lines.splice(insertAt, 0, entry);
  return lines.join("\n");
});
await app.fileManager.processFrontMatter(exp, (fm) => {
  if (fm.status === "planned") fm.status = "in-progress";
  fm.updated = lv.today();
});
await lv.insertLogLine(target, `- Continued [[${exp.basename}]]`);
new Notice(`Logged ${day} in ${exp.basename}`);
-%>
