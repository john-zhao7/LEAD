from __future__ import annotations

from pathlib import Path
from lead.types import CheckpointSummary


def load_checkpoints(run_dir: Path) -> CheckpointSummary | None:
    ckpt_dir = run_dir / "checkpoints"
    if not ckpt_dir.exists():
        return None
    files = sorted(ckpt_dir.glob("*.pt")) + sorted(ckpt_dir.glob("*.ckpt"))
    return CheckpointSummary(count=len(files), latest_step=None, notes="MVP no deep checkpoint introspection")
