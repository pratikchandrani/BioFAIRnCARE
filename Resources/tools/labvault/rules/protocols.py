"""PR rules: experiments cite usable protocol versions; cited versions are not silently edited."""

from __future__ import annotations

from ..frontmatter import link_targets
from ..gitcheck import normalise_body, split_note
from . import finding

DONE = ("completed", "signed-off", "archived")
VOLATILE = {"updated", "status"}


def _cited(ctx):
    v = ctx.vault
    for exp in ctx.typed_notes():
        if exp.type != "experiment":
            continue
        for target in link_targets(exp.data.get("protocols")):
            rel = v.resolve(target, exp.rel)
            prot = v.by_rel.get(rel) if rel else None
            if prot is not None and prot.type == "protocol":
                yield exp, prot


def pr001(ctx):
    for exp, prot in _cited(ctx):
        status = prot.data.get("status")
        if status in ("draft", "validated"):
            yield finding("PR001", "error", exp, f"cites protocol {prot.stem} with status '{status}' "
                          "(only 'active' protocols may be cited)", exp.line_of("protocols"))
        elif status in ("superseded", "retired") and exp.data.get("status") in ("planned", "in-progress"):
            yield finding("PR001", "warning", exp, f"ongoing experiment cites {status} protocol {prot.stem}",
                          exp.line_of("protocols"), "cite the current active version")


def _comparable(text: str):
    data, body = split_note(text)
    return {k: v for k, v in data.items() if k not in VOLATILE}, normalise_body(body)


def pr002(ctx):
    git = ctx.git
    if git is None or not git.available:
        return
    reported = set()
    for exp, prot in _cited(ctx):
        if exp.data.get("status") not in DONE or prot.rel in reported:
            continue
        done_version = next((ver for ver in git.versions(exp.rel)
                             if split_note(ver.content)[0].get("status") in DONE), None)
        if done_version is None:
            continue
        cited_text = git.show_at(done_version.sha, prot.rel)
        if cited_text is None:
            continue
        if _comparable(cited_text) != _comparable(prot.text):
            reported.add(prot.rel)
            yield finding("PR002", "error", prot,
                          f"protocol changed after it was cited by completed experiment {exp.stem}",
                          suggestion="revert and create a new protocol version (New record → protocol version)")


RULES = {"PR001": pr001, "PR002": pr002}
