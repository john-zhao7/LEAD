from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Literal

ConfidenceTier = Literal["direct_evidence", "strong_inference", "weak_hypothesis"]


@dataclass(slots=True)
class MetricPoint:
    step: int
    value: float
    timestamp: datetime | None = None


@dataclass(slots=True)
class MetricSeries:
    name: str
    points: list[MetricPoint] = field(default_factory=list)
    source: str = "unknown"


@dataclass(slots=True)
class LogEvent:
    source: str
    timestamp: datetime | None
    level: str
    message: str
    step: int | None = None


@dataclass(slots=True)
class ConfigSnapshot:
    source: str
    values: dict[str, Any]


@dataclass(slots=True)
class GitChange:
    commit: str | None = None
    branch: str | None = None
    dirty: bool = False
    diff_summary: str | None = None


@dataclass(slots=True)
class CheckpointSummary:
    count: int = 0
    latest_step: int | None = None
    notes: str | None = None


@dataclass(slots=True)
class RolloutSummary:
    episodes: int | None = None
    avg_return: float | None = None
    success_rate: float | None = None
    action_clip_rate: float | None = None
    notes: str | None = None


@dataclass(slots=True)
class ArtifactInventory:
    run_id: str
    present: dict[str, str]
    missing: list[str]
    quality: dict[str, str]


@dataclass(slots=True)
class AlignmentEvent:
    timestamp: datetime | None
    step: int | None
    kind: str
    summary: str
    related_sources: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Anomaly:
    run_id: str
    metric: str
    step: int | None
    severity: float
    description: str
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FailureSignature:
    run_id: str
    name: str
    mechanism: str
    confidence_tier: ConfidenceTier
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Confound:
    run_ids: list[str]
    name: str
    description: str
    severity: float


@dataclass(slots=True)
class ComparabilityAssessment:
    run_ids: list[str]
    comparable: bool
    score: float
    reasons: list[str]
    confounds: list[Confound] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceItem:
    id: str
    source: str
    excerpt: str
    tier: ConfidenceTier


@dataclass(slots=True)
class ConfidenceAssessment:
    tier: ConfidenceTier
    score: float
    rationale: str


@dataclass(slots=True)
class Hypothesis:
    id: str
    statement: str
    supporting_evidence: list[EvidenceItem]
    contradicting_evidence: list[EvidenceItem]
    confidence: ConfidenceAssessment
    mechanistic_rationale: str
    falsification_experiment: str


@dataclass(slots=True)
class ExperimentRecommendation:
    category: Literal["confirmatory", "falsification", "salvage"]
    title: str
    protocol: str
    expected_outcome: str


@dataclass(slots=True)
class ExperimentRun:
    run_id: str
    path: str
    metrics: list[MetricSeries] = field(default_factory=list)
    logs: list[LogEvent] = field(default_factory=list)
    config: ConfigSnapshot | None = None
    git: GitChange | None = None
    checkpoint: CheckpointSummary | None = None
    rollout: RolloutSummary | None = None
    inventory: ArtifactInventory | None = None


@dataclass(slots=True)
class ExperimentSession:
    session_id: str
    created_at: datetime
    project_root: str
    run_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PostMortemReport:
    session_id: str
    experiment_overview: str
    artifacts_quality: str
    timeline_events: list[AlignmentEvent]
    anomalies: list[Anomaly]
    failure_signatures: list[FailureSignature]
    comparability: ComparabilityAssessment | None
    ranked_hypotheses: list[Hypothesis]
    evidence_table: list[EvidenceItem]
    supported_vs_uncertain: str
    recommendations: list[ExperimentRecommendation]
    limitations: str
    final_confidence_summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
