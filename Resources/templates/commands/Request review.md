<%*
/* TEMPLATE-INFO
template_id: TPL-CMD-REQUEST-REVIEW
name: Request review (command)
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
| 1.0.0   | 2026-10-01 | Pratik Chandrani | Mark a completed experiment as ready for reviewer sign-off |
END TEMPLATE-INFO */
// Run inside a completed experiment note: Ctrl/Cmd+Alt+V.
const file = tp.config.target_file;
const fm = (file && app.metadataCache.getFileCache(file)?.frontmatter) || {};
if (fm.type !== "experiment") { new Notice("Open the experiment note you want reviewed first."); return; }
if (fm.status !== "completed") {
  new Notice(`Status is '${fm.status}'. Set status: completed, end_date and outcome first, then request review.`, 8000);
  return;
}
const missing = ["end_date", "outcome"].filter(k => !fm[k] || fm[k] === "pending");
if (missing.length) { new Notice("Fill " + missing.join(" and ") + " before requesting review.", 8000); return; }
await app.fileManager.processFrontMatter(file, (f) => {
  f.review_requested = true;
  f.updated = tp.date.now("YYYY-MM-DD");
});
new Notice("Review requested. Commit and push (Git), then tell your reviewer — it now shows under Experiments → Awaiting review.", 10000);
-%>
