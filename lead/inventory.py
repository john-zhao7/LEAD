from __future__ import annotations

from pathlib import Path
from lead.types import ArtifactInventory


EXPECTED = ["config", "metrics", "stdout", "stderr", "git"]


def build_inventory(run_dir: Path, run_id: str) -> ArtifactInventory:
    present: dict[str, str] = {}
    quality: dict[str, str] = {}

    cfg = next((p for p in [run_dir / "config.yaml", run_dir / "config.yml"] if p.exists()), None)
    if cfg:
        present["config"] = cfg.name
        quality["config"] = "good"

    metrics = None
    for p in [run_dir / "metrics.jsonl", run_dir / "wandb_history.csv", run_dir / "tensorboard_scalars.csv"]:
        if p.exists():
            metrics = p
            break
    if metrics:
        present["metrics"] = metrics.name
        quality["metrics"] = "good"

    if (run_dir / "stdout.log").exists():
        present["stdout"] = "stdout.log"; quality["stdout"] = "medium"
    if (run_dir / "stderr.log").exists():
        present["stderr"] = "stderr.log"; quality["stderr"] = "medium"
    if (run_dir / "git_meta.json").exists() or (run_dir / ".git").exists():
        present["git"] = "git_meta.json|git"; quality["git"] = "good"

    missing = [k for k in EXPECTED if k not in present]
    return ArtifactInventory(run_id=run_id, present=present, missing=missing, quality=quality)
