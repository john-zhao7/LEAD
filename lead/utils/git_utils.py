from __future__ import annotations

from pathlib import Path
import subprocess


def git_cmd(repo: Path, args: list[str]) -> str | None:
    try:
        out = subprocess.check_output(["git", *args], cwd=repo, text=True).strip()
        return out
    except Exception:
        return None
