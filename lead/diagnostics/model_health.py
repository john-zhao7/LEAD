from __future__ import annotations

from lead.types import FailureSignature, RolloutSummary


def robot_health_checks(run_id: str, rollout: RolloutSummary | None) -> list[FailureSignature]:
    out: list[FailureSignature] = []
    if not rollout:
        return out
    if rollout.action_clip_rate is not None and rollout.action_clip_rate > 0.25:
        out.append(FailureSignature(
            run_id=run_id,
            name="action_saturation",
            mechanism="High action clipping indicates policy saturating control bounds",
            confidence_tier="strong_inference",
            evidence_ids=[],
        ))
    if rollout.success_rate is not None and rollout.avg_return is not None and rollout.success_rate > 0.9 and rollout.avg_return < 0:
        out.append(FailureSignature(
            run_id=run_id,
            name="possible_metric_gaming",
            mechanism="High success with low return can indicate reward misspecification or metric gaming",
            confidence_tier="weak_hypothesis",
            evidence_ids=[],
        ))
    return out
