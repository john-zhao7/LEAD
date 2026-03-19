from pathlib import Path
from lead.pipeline import diagnose_single_run


def test_postmortem_sections_present():
    report = diagnose_single_run(Path('tests/fixtures/single_run/run_instability'))
    d = report.to_dict()
    required = ['experiment_overview', 'artifacts_quality', 'timeline_events', 'anomalies', 'ranked_hypotheses', 'final_confidence_summary']
    for k in required:
        assert k in d
