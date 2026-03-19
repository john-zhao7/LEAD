from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class LoaderContext:
    run_dir: Path
    run_id: str
