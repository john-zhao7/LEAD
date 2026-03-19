from __future__ import annotations

from lead.types import ComparabilityAssessment, ExperimentRun
from .confounds import detect_confounds


def assess_comparability(runs: list[ExperimentRun]) -> ComparabilityAssessment:
    run_ids = [r.run_id for r in runs]
    confounds = detect_confounds(runs)
    penalty = sum(c.severity for c in confounds)
    score = max(0.0, 1.0 - min(penalty, 1.0))
    comparable = score >= 0.5 and not any(c.name == "budget_mismatch" for c in confounds)
    reasons = [f"{c.name}: {c.description}" for c in confounds] or ["No major confounds detected"]
    return ComparabilityAssessment(run_ids=run_ids, comparable=comparable, score=score, reasons=reasons, confounds=confounds)
