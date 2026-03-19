from __future__ import annotations

from lead.types import Anomaly, FailureSignature


def infer_failure_signatures(run_id: str, anomalies: list[Anomaly]) -> list[FailureSignature]:
    out: list[FailureSignature] = []
    for a in anomalies:
        if "NaN" in a.description or a.severity > 0.9:
            out.append(FailureSignature(run_id=run_id, name="optimization_instability", mechanism="Potential exploding gradients / unstable optimizer dynamics", confidence_tier="strong_inference", evidence_ids=a.evidence_ids))
        if a.metric in {"success_rate", "episode_reward"} and a.severity > 0.5:
            out.append(FailureSignature(run_id=run_id, name="metric_definition_or_policy_regime_shift", mechanism="Metric trend changed abruptly; check eval protocol or policy mode shift", confidence_tier="weak_hypothesis", evidence_ids=a.evidence_ids))
    return out
