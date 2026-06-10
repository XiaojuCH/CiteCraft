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


@APP.route("/")
def index():
    run = _load_demo_run()
    return render_template("index.html", run=run)


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
