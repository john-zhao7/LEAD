from pathlib import Path
from lead.pipeline import load_run
from lead.diagnostics.anomaly_detector import detect_anomalies
from lead.diagnostics.hypothesis_engine import rank_hypotheses


def test_hypothesis_has_confidence_tier():
    run = load_run(Path('tests/fixtures/single_run/run_instability'))
    anomalies, evidence = detect_anomalies(run)
    hyps = rank_hypotheses(anomalies, evidence)
    assert hyps
    assert hyps[0].confidence.tier in {'direct_evidence', 'strong_inference', 'weak_hypothesis'}
