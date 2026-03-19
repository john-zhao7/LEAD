from pathlib import Path
from lead.pipeline import load_run
from lead.normalize.timeline import reconstruct_timeline


def test_timeline_has_runtime_warning_events():
    run = load_run(Path('tests/fixtures/single_run/run_instability'))
    events = reconstruct_timeline(run)
    assert any(e.kind == 'runtime_warning' for e in events)
