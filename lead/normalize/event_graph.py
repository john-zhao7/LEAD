from __future__ import annotations

from lead.types import AlignmentEvent


def build_event_graph(events: list[AlignmentEvent]) -> dict[str, list[int]]:
    graph: dict[str, list[int]] = {}
    for idx, e in enumerate(events):
        graph.setdefault(e.kind, []).append(idx)
    return graph
