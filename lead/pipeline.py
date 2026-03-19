from __future__ import annotations

from pathlib import Path
import json

from lead.inventory import build_inventory
from lead.ingestion.config_loader import load_config
from lead.ingestion.git_loader import load_git_meta
from lead.ingestion.stdout_loader import parse_log
from lead.ingestion.stderr_loader import load_stderr
from lead.ingestion.wandb_loader import load_wandb_csv
from lead.ingestion.tensorboard_loader import load_tensorboard_scalars
from lead.ingestion.checkpoint_loader import load_checkpoints
from lead.ingestion.rollout_loader import load_rollout_summary
from lead.normalize.canonicalize import canonicalize_metric_names
from lead.normalize.timeline import reconstruct_timeline
from lead.diagnostics.anomaly_detector import detect_anomalies
from lead.diagnostics.failure_signatures import infer_failure_signatures
from lead.diagnostics.model_health import robot_health_checks
from lead.diagnostics.comparability import assess_comparability
from lead.diagnostics.hypothesis_engine import rank_hypotheses
from lead.reports.postmortem import build_postmortem
from lead.types import ExperimentRun, MetricPoint, MetricSeries, PostMortemReport


def _load_metrics_jsonl(run_dir: Path) -> list[MetricSeries]:
    path = run_dir / "metrics.jsonl"
    if not path.exists():
        return []
    by_metric: dict[str, list[MetricPoint]] = {}
    for ln in path.read_text().splitlines():
        if not ln.strip():
            continue
        row = json.loads(ln)
        step = int(row.get("step", 0))
        for k, v in row.items():
            if k in {"step", "timestamp"}:
                continue
            if isinstance(v, (int, float)):
                by_metric.setdefault(k, []).append(MetricPoint(step=step, value=float(v)))
    return [MetricSeries(name=n, points=p, source="metrics_jsonl") for n, p in by_metric.items()]


def load_run(run_dir: Path) -> ExperimentRun:
    run_id = run_dir.name
    inventory = build_inventory(run_dir, run_id)
    metrics = _load_metrics_jsonl(run_dir)
    metrics.extend(load_wandb_csv(run_dir))
    metrics.extend(load_tensorboard_scalars(run_dir))
    metrics = canonicalize_metric_names(metrics)
    logs = parse_log(run_dir / "stdout.log", "stdout") + load_stderr(run_dir)
    run = ExperimentRun(
        run_id=run_id,
        path=str(run_dir),
        metrics=metrics,
        logs=logs,
        config=load_config(run_dir),
        git=load_git_meta(run_dir),
        checkpoint=load_checkpoints(run_dir),
        rollout=load_rollout_summary(run_dir),
        inventory=inventory,
    )
    return run


def diagnose_single_run(run_dir: Path, session_id: str = "adhoc") -> PostMortemReport:
    run = load_run(run_dir)
    timeline = reconstruct_timeline(run)
    anomalies, evidence = detect_anomalies(run)
    signatures = infer_failure_signatures(run.run_id, anomalies)
    signatures += robot_health_checks(run.run_id, run.rollout)
    hypotheses = rank_hypotheses(anomalies, evidence)
    report = build_postmortem(
        session_id=session_id,
        overview=f"Single-run diagnosis for {run.run_id}",
        artifacts_quality=f"Present={run.inventory.present}; Missing={run.inventory.missing}",
        timeline_events=timeline,
        anomalies=anomalies,
        signatures=signatures,
        comparability=None,
        hypotheses=hypotheses,
        evidence=evidence,
    )
    return report


def compare_runs(run_dirs: list[Path], session_id: str = "adhoc") -> PostMortemReport:
    runs = [load_run(p) for p in run_dirs]
    comp = assess_comparability(runs)
    primary = runs[0]
    timeline = reconstruct_timeline(primary)
    anomalies, evidence = detect_anomalies(primary)
    signatures = infer_failure_signatures(primary.run_id, anomalies)
    hypotheses = rank_hypotheses(anomalies, evidence)
    report = build_postmortem(
        session_id=session_id,
        overview=f"Cross-run diagnosis for {[r.run_id for r in runs]}",
        artifacts_quality=f"Comparability score={comp.score:.2f}, comparable={comp.comparable}",
        timeline_events=timeline,
        anomalies=anomalies,
        signatures=signatures,
        comparability=comp,
        hypotheses=hypotheses,
        evidence=evidence,
    )
    return report
