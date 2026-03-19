from __future__ import annotations

import csv
from pathlib import Path
from lead.types import MetricPoint, MetricSeries


def load_tensorboard_scalars(run_dir: Path) -> list[MetricSeries]:
    """MVP loader for exported scalar CSV, not raw event file parsing."""
    path = run_dir / "tensorboard_scalars.csv"
    if not path.exists():
        return []
    by_metric: dict[str, list[MetricPoint]] = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = row.get("tag") or row.get("metric")
            if not tag:
                continue
            step = int(float(row.get("step", 0) or 0))
            value = float(row.get("value", 0) or 0)
            by_metric.setdefault(tag, []).append(MetricPoint(step=step, value=value))
    return [MetricSeries(name=k, points=v, source="tensorboard_csv") for k, v in by_metric.items()]
