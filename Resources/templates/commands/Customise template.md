<%*
/* TEMPLATE-INFO
template_id: TPL-CMD-CUSTOMISE
name: Customise template (command)
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
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Copy a lab template to Resources/note-templates/local/ as a recorded, versioned local customisation |
END TEMPLATE-INFO */
// Ctrl/Cmd+Alt+T. Lab templates are never edited directly: lab updates would overwrite your changes.
const LOCAL_DIR = "Resources/note-templates/local";
const fmOf = (f) => (f && app.metadataCache.getFileCache(f)?.frontmatter) || {};
const settings = fmOf(app.vault.getAbstractFileByPath("Resources/Vault settings.md"));
const today = tp.date.now("YYYY-MM-DD");
const field = (text, key) => ((text.split("END TEMPLATE-INFO")[0].match(new RegExp("^" + key + ":[ \\t]*(.*)$", "m")) || [])[1] || "").trim();

const labFiles = app.vault.getMarkdownFiles()
  .filter(f => /^Resources\/note-templates\/(experiments|records)\//.test(f.path))
  .sort((a, b) => a.path.localeCompare(b.path));
const labels = [];
for (const f of labFiles) labels.push(`${f.basename}  v${field(await app.vault.cachedRead(f), "version")}`);
const src = await tp.system.suggester(labels, labFiles, false, "Which lab template do you want to customise?");
if (!src) return;

const target = `${LOCAL_DIR}/${src.basename}-local.md`;
const existing = app.vault.getAbstractFileByPath(target);
if (existing) {
  new Notice("You already have a local copy — opening it. Bump its version (…-local.N+1) and add a CHANGELOG row when you change it.", 10000);
  await app.workspace.getLeaf("tab").openFile(existing);
  return;
}
const summary = String(await tp.system.prompt("What will you change? (one line, recorded in the template)", "", false) || "").replace(/\n/g, " ").replace(/\*\//g, "").trim();
if (!summary) { new Notice("A short summary is required — nothing copied."); return; }

let text = await app.vault.read(src);
const tid = field(text, "template_id");
const base = field(text, "version");
const localVersion = `${base}-local.1`;
const who = String(settings.owner || "").trim() || "unknown";
const setKey = (t, key, value) => t.replace(new RegExp("^" + key + ":.*$", "m"), `${key}: ${value}`);
let [head, rest] = [text.split("END TEMPLATE-INFO")[0], "END TEMPLATE-INFO" + text.split("END TEMPLATE-INFO").slice(1).join("END TEMPLATE-INFO")];
head = setKey(head, "lab_owned", "false");
head = setKey(head, "version", localVersion);
head = setKey(head, "base_template_id", tid);
head = setKey(head, "base_version", base);
head = setKey(head, "customised_by", who);
head = setKey(head, "customised_on", today);
head = setKey(head, "customisation_summary", summary);
head = head.replace(/\n*$/, "\n") + `| ${localVersion} | ${today} | ${who} | ${summary} |\n`;
rest = rest.replace(/^template_version:.*$/m, `template_version: ${localVersion}`);
text = head + rest;

if (!app.vault.getAbstractFileByPath(LOCAL_DIR)) await app.vault.createFolder(LOCAL_DIR);
const created = await app.vault.create(target, text);
await app.workspace.getLeaf("tab").openFile(created);
new Notice(`Created ${target} (${localVersion}). New experiment / New record will now use your copy.`, 8000);
-%>
