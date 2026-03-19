from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict
from lead.types import ExperimentSession


def save_session(path: Path, session: ExperimentSession) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(session), indent=2, default=str))
