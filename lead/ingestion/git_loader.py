from __future__ import annotations

from pathlib import Path
import json
from lead.types import GitChange
from lead.utils.git_utils import git_cmd


def load_git_meta(run_dir: Path) -> GitChange | None:
    meta = run_dir / "git_meta.json"
    if meta.exists():
        try:
            data = json.loads(meta.read_text())
            return GitChange(
                commit=data.get("commit"),
                branch=data.get("branch"),
                dirty=bool(data.get("dirty", False)),
                diff_summary=data.get("diff_summary"),
            )
        except Exception:
            pass
    commit = git_cmd(run_dir, ["rev-parse", "HEAD"])
    if not commit:
        return None
    branch = git_cmd(run_dir, ["rev-parse", "--abbrev-ref", "HEAD"])
    dirty = bool(git_cmd(run_dir, ["status", "--porcelain"]))
    return GitChange(commit=commit, branch=branch, dirty=dirty, diff_summary=None)
