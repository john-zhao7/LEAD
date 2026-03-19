from pathlib import Path
from lead.pipeline import load_run
from lead.diagnostics.comparability import assess_comparability


def test_detect_budget_confound():
    r1 = load_run(Path('tests/fixtures/multi_run/run_a'))
    r2 = load_run(Path('tests/fixtures/multi_run/run_b'))
    comp = assess_comparability([r1, r2])
    assert any(c.name == 'budget_mismatch' for c in comp.confounds)
    assert comp.comparable is False
