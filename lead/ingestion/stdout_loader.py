from __future__ import annotations

from datetime import datetime
from pathlib import Path
from lead.types import LogEvent


def parse_log(path: Path, source: str) -> list[LogEvent]:
    out: list[LogEvent] = []
    if not path.exists():
        return out
    for ln in path.read_text(errors="ignore").splitlines():
        level = "INFO"
        msg = ln
        if "WARN" in ln.upper():
            level = "WARN"
        if "ERROR" in ln.upper() or "TRACEBACK" in ln.upper():
            level = "ERROR"
        out.append(LogEvent(source=source, timestamp=None, level=level, message=msg))
    return out
