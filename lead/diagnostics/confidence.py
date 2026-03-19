from __future__ import annotations

from lead.types import ConfidenceAssessment


def make_confidence(score: float, rationale: str) -> ConfidenceAssessment:
    if score >= 0.75:
        tier = "direct_evidence"
    elif score >= 0.45:
        tier = "strong_inference"
    else:
        tier = "weak_hypothesis"
    return ConfidenceAssessment(tier=tier, score=round(score, 3), rationale=rationale)
