from __future__ import annotations

from pathlib import Path


def append_history(path: Path, entry: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(entry.rstrip() + "
")
