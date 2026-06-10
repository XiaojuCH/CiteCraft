"""Helpers for flattening traces out of structured deliverables."""

from __future__ import annotations

from typing import List


def collect_traces(deliverable) -> List:
    traces = []
    if deliverable.deliverable_type == "brief":
        for section in deliverable.sections:
            for item in section.items:
                traces.extend(item.trace_refs)
    elif deliverable.deliverable_type == "literature_matrix":
        for cell in deliverable.cells:
            traces.extend(cell.trace_refs)
        for node in deliverable.synthesis:
            traces.extend(node.trace_refs)
    elif deliverable.deliverable_type == "slides":
        for slide in deliverable.slides:
            for bullet in slide.bullets:
                traces.extend(bullet.trace_refs)
            for note in slide.speaker_notes:
                traces.extend(note.trace_refs)
    return traces

