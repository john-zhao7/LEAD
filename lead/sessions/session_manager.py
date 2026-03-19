from __future__ import annotations

from datetime import datetime
from pathlib import Path
from lead.types import ExperimentSession
from .storage import save_session


def init_session(project_root: Path, session_id: str) -> ExperimentSession:
    sess = ExperimentSession(session_id=session_id, created_at=datetime.utcnow(), project_root=str(project_root))
    save_session(project_root / ".lead_session" / f"{session_id}.json", sess)
    return sess
