from __future__ import annotations

from pathlib import Path
import json
from lead.types import RolloutSummary


def load_rollout_summary(run_dir: Path) -> RolloutSummary | None:
    path = run_dir / "rollout_summary.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return RolloutSummary(
        episodes=data.get("episodes"),
        avg_return=data.get("avg_return"),
        success_rate=data.get("success_rate"),
        action_clip_rate=data.get("action_clip_rate"),
        notes=data.get("notes"),
    )
