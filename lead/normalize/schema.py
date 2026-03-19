from __future__ import annotations

from lead.types import ExperimentRun


def validate_run_schema(run: ExperimentRun) -> list[str]:
    issues: list[str] = []
    if not run.metrics:
        issues.append("missing_metrics")
    if not run.config:
        issues.append("missing_config")
    return issues
