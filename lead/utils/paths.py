from __future__ import annotations

from pathlib import Path


def find_first(path: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        p = path / name
        if p.exists():
            return p
    return None
