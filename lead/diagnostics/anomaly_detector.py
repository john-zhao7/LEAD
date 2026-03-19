from __future__ import annotations

from statistics import median
from lead.types import Anomaly, EvidenceItem, ExperimentRun


def detect_anomalies(run: ExperimentRun) -> tuple[list[Anomaly], list[EvidenceItem]]:
    anomalies: list[Anomaly] = []
    evidence: list[EvidenceItem] = []
    eid = 0
    for s in run.metrics:
        vals = [p.value for p in s.points]
        if len(vals) < 4:
            continue
        baseline = median(vals[: max(2, len(vals)//4)])
        for p in s.points:
            if baseline == 0:
                continue
            delta = abs((p.value - baseline) / baseline)
            if delta > 2.0:
                ev_id = f"ev-{eid}"; eid += 1
                evidence.append(EvidenceItem(id=ev_id, source=s.source, excerpt=f"{s.name} jump at step {p.step}: {p.value} vs baseline {baseline}", tier="direct_evidence"))
                anomalies.append(Anomaly(run_id=run.run_id, metric=s.name, step=p.step, severity=min(delta/5,1), description=f"Large deviation in {s.name}", evidence_ids=[ev_id]))
                break
        if any(p.value != p.value for p in s.points):
            ev_id = f"ev-{eid}"; eid += 1
            evidence.append(EvidenceItem(id=ev_id, source=s.source, excerpt=f"NaN detected in {s.name}", tier="direct_evidence"))
            anomalies.append(Anomaly(run_id=run.run_id, metric=s.name, step=None, severity=1.0, description="NaN metric detected", evidence_ids=[ev_id]))
    for lg in run.logs:
        if lg.level == "ERROR":
            ev_id = f"ev-{eid}"; eid += 1
            evidence.append(EvidenceItem(id=ev_id, source=lg.source, excerpt=lg.message[:180], tier="direct_evidence"))
            anomalies.append(Anomaly(run_id=run.run_id, metric="runtime", step=lg.step, severity=0.8, description="Runtime error present", evidence_ids=[ev_id]))
    return anomalies, evidence
