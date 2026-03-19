from __future__ import annotations

from lead.types import Anomaly, EvidenceItem, Hypothesis
from .confidence import make_confidence


def rank_hypotheses(anomalies: list[Anomaly], evidence: list[EvidenceItem]) -> list[Hypothesis]:
    hyps: list[Hypothesis] = []
    if not anomalies:
        return hyps
    first = anomalies[0]
    support = [e for e in evidence if e.id in first.evidence_ids] or evidence[:1]
    score = min(0.9, 0.4 + 0.15 * len(support) + 0.1 * first.severity)
    hyps.append(Hypothesis(
        id="hyp-0",
        statement=f"Primary failure likely driven by {first.metric} instability near step {first.step}",
        supporting_evidence=support,
        contradicting_evidence=[],
        confidence=make_confidence(score, "Evidence from anomaly onset + log correlation"),
        mechanistic_rationale="Abrupt metric shift with runtime warnings is consistent with optimizer instability or data pipeline discontinuity.",
        falsification_experiment="Repeat with LR x0.3 and gradient clipping=1.0 while holding seed and budget fixed.",
    ))
    if any("runtime" == a.metric for a in anomalies):
        hyps.append(Hypothesis(
            id="hyp-1",
            statement="Runtime failure contributed materially to degraded learning dynamics",
            supporting_evidence=[e for e in evidence if "error" in e.excerpt.lower()][:2],
            contradicting_evidence=[],
            confidence=make_confidence(0.7, "Direct runtime error evidence"),
            mechanistic_rationale="Process-level instability can truncate updates and bias replay/sample distribution.",
            falsification_experiment="Rerun same config with runtime warnings resolved; compare anomaly onset timing.",
        ))
    hyps.sort(key=lambda h: h.confidence.score, reverse=True)
    return hyps
