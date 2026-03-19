from __future__ import annotations

from lead.types import MetricSeries


def canonicalize_metric_names(metrics: list[MetricSeries]) -> list[MetricSeries]:
    aliases = {
        "train/loss": "loss",
        "loss/train": "loss",
        "eval/success_rate": "success_rate",
    }
    for m in metrics:
        m.name = aliases.get(m.name, m.name)
    return metrics
