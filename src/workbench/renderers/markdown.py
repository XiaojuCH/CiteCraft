"""Markdown renderers for deliverables."""

from __future__ import annotations

from typing import Iterable


def _trace_suffix(trace_refs: Iterable) -> str:
    labels = [trace.locator.label for trace in trace_refs]
    if not labels:
        return ""
    return " _(Trace: %s)_" % ", ".join(labels)


def render_brief(deliverable) -> str:
    lines = ["# %s" % deliverable.title, "", deliverable.objective, ""]
    for section in deliverable.sections:
        lines.append("## %s" % section.title)
        lines.append("")
        for item in section.items:
            label = "**%s:** " % item.title if item.title else ""
            lines.append("- %s%s%s" % (label, item.text, _trace_suffix(item.trace_refs)))
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_matrix(deliverable) -> str:
    column_labels = ["Source"] + [column.label for column in deliverable.columns]
    header = "| " + " | ".join(column_labels) + " |"
    divider = "| " + " | ".join(["---"] * len(column_labels)) + " |"
    lines = ["# %s" % deliverable.title, "", header, divider]
    cell_lookup = {(cell.row_id, cell.column_id): cell for cell in deliverable.cells}
    for row in deliverable.rows:
        values = [row.label]
        for column in deliverable.columns:
            cell = cell_lookup[(row.row_id, column.column_id)]
            suffix = _trace_suffix(cell.trace_refs) if cell.is_factual else ""
            values.append((cell.value + suffix).replace("\n", " "))
        lines.append("| " + " | ".join(values) + " |")
    lines.extend(["", "## Synthesis", ""])
    for node in deliverable.synthesis:
        lines.append("- **%s:** %s%s" % (node.title, node.text, _trace_suffix(node.trace_refs)))
    lines.append("")
    return "\n".join(lines)


def render_slides(deliverable) -> str:
    lines = ["# %s" % deliverable.title, "", deliverable.deck_goal, "", "## Outline", ""]
    for item in deliverable.outline:
        lines.append("- **%s:** %s" % (item.title, item.purpose))
    lines.append("")
    for slide in deliverable.slides:
        lines.append("## Slide %d: %s" % (slide.slide_number, slide.title))
        lines.append("")
        for bullet in slide.bullets:
            lines.append("- %s%s" % (bullet.text, _trace_suffix(bullet.trace_refs)))
        if slide.speaker_notes:
            lines.append("")
            lines.append("Speaker notes:")
            for note in slide.speaker_notes:
                lines.append("- %s%s" % (note.text, _trace_suffix(note.trace_refs)))
        lines.append("")
    return "\n".join(lines).strip() + "\n"

