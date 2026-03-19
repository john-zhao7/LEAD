from __future__ import annotations

from pathlib import Path
from lead.ingestion.stdout_loader import parse_log
from lead.types import LogEvent


def load_stderr(run_dir: Path) -> list[LogEvent]:
    return parse_log(run_dir / "stderr.log", "stderr")
