from __future__ import annotations

from lead.types import ExperimentRun


def summarize_cross_run_effects(runs: list[ExperimentRun]) -> str:
    if len(runs) < 2:
        return "Insufficient runs for cross-run effect synthesis."
    return "MVP synthesis: compare terminal metric deltas only after comparability gate passes."
