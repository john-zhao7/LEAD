from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class LeadConfig:
    project_root: Path
    session_dir: Path
    passive_mode: bool = True

    @classmethod
    def from_project(cls, project_root: str | Path) -> "LeadConfig":
        root = Path(project_root).resolve()
        return cls(project_root=root, session_dir=root / ".lead_session", passive_mode=True)
