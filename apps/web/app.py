"""Flask demo shell for the golden-path sample project."""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, abort, render_template

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from workbench.pipeline.run import run_project  # noqa: E402
from workbench.renderers.traces import collect_traces  # noqa: E402


APP = Flask(
    __name__,
    template_folder=str(Path(__file__).resolve().parent / "templates"),
    static_folder=str(Path(__file__).resolve().parent / "static"),
)
PROJECT_ROOT = REPO_ROOT / "examples" / "academia" / "demo-01"


def _load_demo_run():
    return run_project(PROJECT_ROOT)


def _homepage_payload(run):
    brief = run.deliverables["brief"]
    matrix = run.deliverables["literature_matrix"]
    slides = run.deliverables["slides"]
    first_row = matrix.rows[0]
    cell_lookup = {(cell.row_id, cell.column_id): cell for cell in matrix.cells}
    matrix_columns = []
    for column in matrix.columns[:3]:
        cell = cell_lookup[(first_row.row_id, column.column_id)]
        matrix_columns.append(
            {
                "label": column.label,
                "value": cell.value,
                "trace_label": cell.trace_refs[0].locator.label if cell.trace_refs else "Narrative",
            }
        )

    first_slide = slides.slides[0]
    total_chunks = sum(len(document.chunks) for document in run.documents)
    return {
        "metrics": [
            {"label_en": "Sources", "label_zh": "输入源", "value": str(len(run.documents))},
            {"label_en": "Chunks", "label_zh": "源片段", "value": str(total_chunks)},
            {"label_en": "Trace links", "label_zh": "可追溯链接", "value": str(len(run.trace_index))},
        ],
        "brief": {
            "summary": brief.sections[0].items[0],
            "finding": brief.sections[1].items[0],
        },
        "matrix": {
            "row_label": first_row.label,
            "columns": matrix_columns,
        },
        "slides": {
            "title": first_slide.title,
            "bullets": first_slide.bullets[:2],
            "notes": first_slide.speaker_notes[:1],
        },
    }


@APP.route("/")
def index():
    run = _load_demo_run()
    return render_template("index.html", run=run, homepage=_homepage_payload(run))


@APP.route("/sources")
def sources_index():
    run = _load_demo_run()
    return render_template("sources.html", run=run)


@APP.route("/sources/<source_id>")
def source_view(source_id: str):
    run = _load_demo_run()
    document = next((item for item in run.documents if item.source_id == source_id), None)
    if document is None:
        abort(404)
    return render_template(
        "source.html",
        run=run,
        document=document,
    )


@APP.route("/deliverables/<deliverable_key>")
def deliverable_view(deliverable_key: str):
    run = _load_demo_run()
    if deliverable_key not in run.deliverables:
        abort(404)
    deliverable = run.deliverables[deliverable_key]
    content_html = run.html_outputs[deliverable_key]
    traces = collect_traces(deliverable)
    return render_template(
        "deliverable.html",
        run=run,
        deliverable_key=deliverable_key,
        deliverable=deliverable,
        content_html=content_html,
        traces=traces,
    )


@APP.route("/traces/<trace_id>")
def trace_view(trace_id: str):
    run = _load_demo_run()
    trace = run.trace_index.get(trace_id)
    if trace is None:
        abort(404)
    chunk = run.chunk_index.get(trace.chunk_id)
    if chunk is None:
        abort(404)
    return render_template(
        "trace.html",
        run=run,
        trace=trace,
        chunk=chunk,
    )


if __name__ == "__main__":
    APP.run(debug=True)
