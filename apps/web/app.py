"""Flask demo shell for the golden-path sample project."""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, abort, g, render_template, request, url_for

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
WEB_ROOT = Path(__file__).resolve().parent
if str(WEB_ROOT) not in sys.path:
    sys.path.insert(0, str(WEB_ROOT))

from i18n import DEFAULT_LANG, normalize_lang, translate  # noqa: E402
from workbench.pipeline.run import run_project  # noqa: E402
from workbench.renderers.traces import collect_traces  # noqa: E402


APP = Flask(
    __name__,
    template_folder=str(Path(__file__).resolve().parent / "templates"),
    static_folder=str(Path(__file__).resolve().parent / "static"),
)
PROJECT_ROOT = REPO_ROOT / "examples" / "academia" / "demo-01"


@APP.before_request
def set_lang():
    requested = request.args.get("lang")
    if requested:
        g.lang = normalize_lang(requested)
        g.persist_lang = True
    else:
        g.lang = normalize_lang(request.cookies.get("workbench_lang", DEFAULT_LANG))
        g.persist_lang = False


@APP.after_request
def persist_lang(response):
    if getattr(g, "persist_lang", False):
        response.set_cookie("workbench_lang", g.lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response


@APP.context_processor
def inject_template_helpers():
    def t(key: str) -> str:
        return translate(g.lang, key)

    def shell_url(endpoint: str, **values) -> str:
        values["lang"] = g.lang
        return url_for(endpoint, **values)

    def toggle_lang_url(target_lang: str) -> str:
        values = dict(request.view_args or {})
        for key, value in request.args.items():
            if key != "lang":
                values[key] = value
        values["lang"] = normalize_lang(target_lang)
        return url_for(request.endpoint or "index", **values)

    return {
        "lang": g.lang,
        "html_lang": "zh-CN" if g.lang == "zh" else "en",
        "t": t,
        "shell_url": shell_url,
        "toggle_lang_url": toggle_lang_url,
    }


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
            }
        )

    first_slide = slides.slides[0]
    total_chunks = sum(len(document.chunks) for document in run.documents)
    return {
        "metrics": [
            {"label_key": "metric_sources", "value": str(len(run.documents))},
            {"label_key": "metric_chunks", "value": str(total_chunks)},
            {"label_key": "metric_trace_links", "value": str(len(run.trace_index))},
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
