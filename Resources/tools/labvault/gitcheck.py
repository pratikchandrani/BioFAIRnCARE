"""Read-only access to Git history through the system `git` executable (research R9)."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from . import frontmatter as fmlib


@dataclass
class Version:
    sha: str
    email: str
    date: datetime
    path: str  # repo-relative path at that commit
    content: str


class Git:
    def __init__(self, vault_root: Path):
        self.vault_root = vault_root.resolve()
        self.available = False
        self.top: Path | None = None
        self._cache: dict[str, list[Version]] = {}
        if shutil.which("git") is None:
            return
        out = self._run(["rev-parse", "--show-toplevel"], cwd=self.vault_root)
        if out is None:
            return
        self.top = Path(out.strip()).resolve()
        self.available = True

    def _run(self, args: list[str], cwd: Path | None = None) -> str | None:
        try:
            proc = subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=str(cwd or self.top),
                                  capture_output=True, text=True, encoding="utf-8", errors="replace",
                                  timeout=60)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return proc.stdout if proc.returncode == 0 else None

    def repo_path(self, vault_rel: str) -> str:
        return (self.vault_root / vault_rel).resolve().relative_to(self.top).as_posix()

    def show_at(self, sha: str, vault_rel: str) -> str | None:
        """Content of a file as of commit `sha` (None if it did not exist there)."""
        if not self.available:
            return None
        return self._run(["show", f"{sha}:{self.repo_path(vault_rel)}"])

    def versions(self, vault_rel: str) -> list[Version]:
        """Committed versions of a file, oldest first, following renames."""
        if not self.available:
            return []
        if vault_rel in self._cache:
            return self._cache[vault_rel]
        log = self._run(["log", "--follow", "--format=@@%H\x1f%ae\x1f%aI", "--name-only", "--",
                         self.repo_path(vault_rel)])
        versions: list[Version] = []
        if log:
            entries = [e for e in log.split("@@") if e.strip()]
            for entry in entries:
                lines = [ln for ln in entry.strip("\n").split("\n") if ln.strip()]
                sha, email, date = lines[0].split("\x1f")
                path = lines[1] if len(lines) > 1 else self.repo_path(vault_rel)
                content = self._run(["show", f"{sha}:{path}"])
                if content is None:
                    continue  # deleted in this commit
                versions.append(Version(sha=sha, email=email.lower(), date=datetime.fromisoformat(date),
                                        path=path, content=content))
        versions.reverse()
        self._cache[vault_rel] = versions
        return versions


def split_note(text: str) -> tuple[dict, str]:
    """(frontmatter dict, body) of a note's text; invalid frontmatter -> ({}, text)."""
    try:
        fm = fmlib.parse(text.replace("\r\n", "\n"))
    except fmlib.FrontmatterError:
        return {}, text
    return dict(fm.data), fm.body


def normalise_body(body: str) -> str:
    lines = [ln.rstrip() for ln in body.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


def before_heading(body: str, heading: str) -> tuple[str, str]:
    """Split body at the first line equal to `heading` (e.g. '## Amendments')."""
    lines = body.replace("\r\n", "\n").split("\n")
    for i, ln in enumerate(lines):
        if ln.strip() == heading:
            return "\n".join(lines[:i]), "\n".join(lines[i:])
    return body, ""
