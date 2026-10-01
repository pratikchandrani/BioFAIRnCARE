// BioFAIRnCARE action buttons (Dataview view script).
// Usage in a note:  await dv.view("Resources/lab_resources/scripts/lab-buttons", { buttons: ["new-experiment", "log", "new-record"] })
// Also registers window.labvaultRun(commandId, { openDaily }) for other blocks (e.g. Home).
//
// Templater commands insert text at the cursor, so they fail with "No active editor" when the note
// is in Reading view or nothing has focus. runInEditor() makes sure an editor exists first:
// it optionally opens today's daily note, switches the note to editing mode and focuses it before
// running the command. Where the log line goes is decided by the command (labvault-commands.js).

const CMD = "templater-obsidian:Resources/templates/commands/";
const BUTTONS = {
  "new-experiment": ["🧪 New experiment", CMD + "New experiment.md"],
  "log": ["📝 Log to experiment", CMD + "Log to experiment.md"],
  "new-record": ["📦 New record", CMD + "New record.md"],
  "request-review": ["✅ Request review", CMD + "Request review.md"],
  "customise": ["🛠️ Customise template", CMD + "Customise template.md"],
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForMarkdownLeaf(predicate, timeoutMs = 3000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const leaf = app.workspace.getMostRecentLeaf();
    if (leaf && leaf.view && leaf.view.getViewType() === "markdown" && (!predicate || predicate(leaf))) return leaf;
    await sleep(100);
  }
  return null;
}

async function runInEditor(commandId, options = {}) {
  let leaf = null;
  if (options.openDaily) {
    const today = window.moment().format("YYYY-MM-DD");
    app.commands.executeCommandById("daily-notes");
    leaf = await waitForMarkdownLeaf((l) => l.view.file && l.view.file.basename === today);
  } else {
    leaf = await waitForMarkdownLeaf(null, 500);
  }
  if (!leaf) {
    new Notice("Open a note first (for example today's daily note), then try again.", 8000);
    return;
  }
  const view = leaf.view;
  if (typeof view.getMode === "function" && view.getMode() === "preview") {
    const vs = leaf.getViewState();
    await leaf.setViewState({ ...vs, state: { ...vs.state, mode: "source" } });
    await sleep(150);
  }
  app.workspace.setActiveLeaf(leaf, { focus: true });
  const editor = leaf.view.editor;
  if (!editor) {
    new Notice("Could not open an editor for this note. Press Ctrl/Cmd+E to switch to editing mode and try again.", 8000);
    return;
  }
  editor.focus();
  if (!app.commands.executeCommandById(commandId)) {
    new Notice("Command not found — check that the Templater plugin is enabled.", 8000);
  }
}

window.labvaultRun = runInEditor;

const wanted = (input && input.buttons) || [];
if (wanted.length) {
  const row = dv.el("div", "", { cls: "lab-buttons" });
  for (const key of wanted) {
    const spec = BUTTONS[key];
    if (!spec) continue;
    const b = row.createEl("button", { text: spec[0], cls: "lab-button" });
    b.onclick = () => runInEditor(spec[1], { openDaily: !!(input && input.openDaily) });
  }
}
