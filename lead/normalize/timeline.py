from __future__ import annotations

from lead.types import AlignmentEvent, ExperimentRun


def reconstruct_timeline(run: ExperimentRun) -> list[AlignmentEvent]:
    events: list[AlignmentEvent] = []
    for series in run.metrics:
        if not series.points:
            continue
        first = series.points[0]
        last = series.points[-1]
        events.append(AlignmentEvent(timestamp=None, step=first.step, kind="metric_start", summary=f"{series.name} starts at {first.value}", related_sources=[series.source]))
        events.append(AlignmentEvent(timestamp=None, step=last.step, kind="metric_end", summary=f"{series.name} ends at {last.value}", related_sources=[series.source]))
    for log in run.logs:
        if log.level in {"WARN", "ERROR"}:
            events.append(AlignmentEvent(timestamp=log.timestamp, step=log.step, kind="runtime_warning", summary=log.message[:160], related_sources=[log.source]))
    events.sort(key=lambda e: (e.step is None, e.step or 0))
    return events
