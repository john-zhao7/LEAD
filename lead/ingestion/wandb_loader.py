from __future__ import annotations

import csv
from pathlib import Path
from lead.types import MetricPoint, MetricSeries


def load_wandb_csv(run_dir: Path) -> list[MetricSeries]:
    path = run_dir / "wandb_history.csv"
    if not path.exists():
        return []
    by_metric: dict[str, list[MetricPoint]] = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            step = int(float(row.get("step", row.get("_step", 0)) or 0))
            for k, v in row.items():
                if k in {"step", "_step", "timestamp", "_timestamp"}:
                    continue
                if v in (None, ""):
                    continue
                try:
                    val = float(v)
                except ValueError:
                    continue
                by_metric.setdefault(k, []).append(MetricPoint(step=step, value=val))
    return [MetricSeries(name=k, points=pts, source="wandb_csv") for k, pts in by_metric.items()]
