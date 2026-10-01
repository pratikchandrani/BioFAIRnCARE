// Shared logic for the BioFAIRnCARE Templater commands (contract: specs/003-experiment-launch-flow/contracts/command-behaviour.md).
// Loaded by each command template:
//   const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
//   const lv = await new AsyncFunction("app", "tp", await app.vault.adapter.read("Resources/lab_resources/scripts/labvault-commands.js"))(app, tp);
// Uses the Obsidian API only (works on desktop and mobile).

const SETTINGS = "Resources/Vault settings.md";
const NOTE_TEMPLATES = "Resources/note-templates/";
const LOCAL = NOTE_TEMPLATES + "local/";
const DAILY_TEMPLATE = "Resources/templates/daily.md";
const EXAMPLE_DAILY = "_Examples/daily_notes/";
const START = "## Daily work updates";
const END = "## End of daily work updates";

const fmOf = (f) => (f && app.metadataCache.getFileCache(f)?.frontmatter) || {};
const today = () => window.moment().format("YYYY-MM-DD");

function parseInfo(text) {
  const block = (text.split("/* TEMPLATE-INFO")[1] || "").split("CHANGELOG")[0];
  const info = {};
  for (const line of block.split("\n")) {
    const i = line.indexOf(":");
    if (i > 0) info[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return info;
}

function settings() {
  return fmOf(app.vault.getAbstractFileByPath(SETTINGS));
}

function initials() {
  const ini = String(settings().owner_initials || "").trim().toUpperCase();
  if (!/^[A-Z]{2,4}$/.test(ini)) {
    new Notice("Set owner_initials (2–4 capital letters, as in Lab members) in Resources/Vault settings.md first.", 10000);
    return null;
  }
  return ini;
}

function sanitize(title, max = 60) {
  return String(title || "").replace(/[\\/:*?"<>|#^\[\]]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
}

// Next sequence number for <prefix>-<ini>-<yyyymmdd>-NN, looking at `id` properties,
// ID-first file names and title-first suffixes (_<ini>-<yyyymmdd>-NN).
function nextId(prefix, ini, yyyymmdd) {
  const head = `${prefix}-${ini}-${yyyymmdd}-`;
  const tail = `_${ini}-${yyyymmdd}-`;
  let max = 0;
  const bump = (s) => { const n = parseInt(String(s).slice(0, 2), 10); if (n > max) max = n; };
  for (const f of app.vault.getMarkdownFiles()) {
    const id = String(fmOf(f).id || "");
    if (id.startsWith(head)) bump(id.slice(head.length));
    if (f.basename.startsWith(head)) bump(f.basename.slice(head.length));
    const i = f.basename.lastIndexOf(tail);
    if (i >= 0) bump(f.basename.slice(i + tail.length));
  }
  if (max >= 99) { new Notice("99 records already created today with these initials — ask the maintainer."); return null; }
  return { id: head + String(max + 1).padStart(2, "0"), nn: String(max + 1).padStart(2, "0") };
}

async function dailyFolder() {
  try {
    const cfg = JSON.parse(await app.vault.adapter.read(app.vault.configDir + "/daily-notes.json"));
    return String(cfg.folder || "daily_notes").replace(/^\/+|\/+$/g, "");
  } catch (e) {
    return "daily_notes";
  }
}

async function isDaily(file) {
  if (!file || file.extension !== "md" || !/^\d{4}-\d{2}-\d{2}$/.test(file.basename)) return false;
  const folder = await dailyFolder();
  return file.path.startsWith(folder + "/") || file.path.startsWith(EXAMPLE_DAILY) || fmOf(file).type === "daily";
}

// The daily note that receives the log line: the active note if it is a daily note (any date),
// otherwise today's daily note, created from the daily template if it does not exist yet.
async function targetDaily() {
  const active = tp.config.target_file || app.workspace.getActiveFile();
  if (await isDaily(active)) {
    return { file: active, date: active.basename, isActive: true, example: active.path.startsWith("_Examples/") };
  }
  const folder = await dailyFolder();
  const date = today();
  let file = app.vault.getAbstractFileByPath(`${folder}/${date}.md`);
  if (!file) {
    const tpl = app.vault.getAbstractFileByPath(DAILY_TEMPLATE);
    if (!app.vault.getAbstractFileByPath(folder)) await app.vault.createFolder(folder);
    file = await tp.file.create_new(tpl, date, false, folder);
    new Notice(`Created today's daily note (${date}).`);
  }
  return { file, date, isActive: false, example: false };
}

function sectionBounds(lines) {
  return { start: lines.findIndex((l) => l.trim() === START), end: lines.findIndex((l) => l.trim() === END) };
}

function insertBeforeEnd(text, line) {
  const lines = text.split("\n");
  if (lines.some((l) => l.trim() === line.trim())) return text;
  const { end } = sectionBounds(lines);
  if (end < 0) return text.replace(/\s*$/, "") + "\n" + line + "\n";
  let at = end;
  while (at > 0 && lines[at - 1].trim() === "") at--;
  lines.splice(at, 0, line);
  if (lines[at + 1] !== undefined && lines[at + 1].trim() !== "") lines.splice(at + 1, 0, "");
  return lines.join("\n");
}

// Insert one log line into the target daily note. At the cursor when the target is the open note
// and the cursor is inside "Daily work updates"; otherwise just before "End of daily work updates".
// Never writes into the frontmatter; never adds an identical line twice.
async function insertLogLine(target, line) {
  const editor = target.isActive ? app.workspace.activeEditor?.editor : null;
  if (editor) {
    const lines = editor.getValue().split("\n");
    if (lines.some((l) => l.trim() === line.trim())) return;
    const { start, end } = sectionBounds(lines);
    const cur = editor.getCursor();
    if (start >= 0 && end > start && cur.line > start && cur.line < end) {
      const current = editor.getLine(cur.line);
      if (current.trim() === "") {
        editor.replaceRange(line, { line: cur.line, ch: 0 }, { line: cur.line, ch: current.length });
      } else {
        editor.replaceRange("\n" + line, { line: cur.line, ch: current.length });
      }
      return;
    }
    const updated = insertBeforeEnd(editor.getValue(), line);
    if (updated !== editor.getValue()) editor.setValue(updated);
    return;
  }
  await app.vault.process(target.file, (text) => insertBeforeEnd(text, line));
}

// Templates of a kind ("experiments" | "records"), preferring a local copy with the same base id.
async function listTemplates(kind) {
  const out = {};
  for (const f of app.vault.getMarkdownFiles().filter((f) => f.path.startsWith(NOTE_TEMPLATES + kind + "/"))) {
    const info = parseInfo(await app.vault.cachedRead(f));
    if (info.template_id && info.status !== "retired") out[info.template_id] = { file: f, info, local: false };
  }
  for (const f of app.vault.getMarkdownFiles().filter((f) => f.path.startsWith(LOCAL))) {
    const info = parseInfo(await app.vault.cachedRead(f));
    if (info.base_template_id && out[info.base_template_id] && info.status !== "retired") {
      out[info.base_template_id] = { file: f, info, local: true };
    }
  }
  return out;
}

return { settings, initials, sanitize, nextId, dailyFolder, isDaily, targetDaily, insertLogLine, listTemplates, parseInfo, today, fmOf };
