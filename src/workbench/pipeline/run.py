"""Run the deterministic pipeline for a project directory."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Dict, List

from workbench.contracts.project import ProjectConfig, load_project_config
from workbench.core.serialization import write_json
from workbench.deliverables.registry import generate_deliverables
from workbench.evidence.index import EvidenceIndex
from workbench.providers.registry import get_provider
from workbench.renderers.html import render_brief_html, render_matrix_html, render_slides_html
from workbench.renderers.markdown import render_brief, render_matrix, render_slides
from workbench.renderers.traces import collect_traces
from workbench.sources.registry import load_documents


@dataclass
class PipelineRun:
    project: ProjectConfig
    documents: List
    deliverables: Dict[str, object]
    markdown_outputs: Dict[str, str]
    html_outputs: Dict[str, str]
    trace_index: Dict[str, object]
    chunk_index: Dict[str, object]
    provider_name: str


def run_project(project_root: Path, provider_name: str = None) -> PipelineRun:
    project = load_project_config(project_root)
    documents = load_documents(project)
    evidence_index = EvidenceIndex(documents)
    provider_name = provider_name or os.environ.get("WORKBENCH_PROVIDER", "deterministic")
    provider = get_provider(provider_name)
    deliverables = generate_deliverables(project, documents, evidence_index, provider)
    markdown_outputs = {
        "brief": render_brief(deliverables["brief"]),
        "literature_matrix": render_matrix(deliverables["literature_matrix"]),
        "slides": render_slides(deliverables["slides"]),
    }
    html_outputs = {
        "brief": render_brief_html(deliverables["brief"]),
        "literature_matrix": render_matrix_html(deliverables["literature_matrix"]),
        "slides": render_slides_html(deliverables["slides"]),
    }
    trace_index = {}
    chunk_index = {}
    for document in documents:
        for chunk in document.chunks:
            chunk_index[chunk.chunk_id] = chunk
    for deliverable in deliverables.values():
        for trace in collect_traces(deliverable):
            trace_index[trace.trace_id] = trace
    return PipelineRun(
        project=project,
        documents=documents,
        deliverables=deliverables,
        markdown_outputs=markdown_outputs,
        html_outputs=html_outputs,
        trace_index=trace_index,
        chunk_index=chunk_index,
        provider_name=provider_name,
    )


def write_outputs(run: PipelineRun, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, deliverable in run.deliverables.items():
        write_json(output_dir / ("%s.json" % key), deliverable)
        (output_dir / ("%s.md" % key)).write_text(run.markdown_outputs[key], encoding="utf-8")
        (output_dir / ("%s.html" % key)).write_text(run.html_outputs[key], encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic deliverables pipeline.")
    parser.add_argument("project_root", help="Path to a sample project.")
    parser.add_argument("--output-dir", help="Optional output directory for generated artifacts.")
    parser.add_argument("--provider", help="Generation provider name.", default=None)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    run = run_project(project_root, provider_name=args.provider)
    if args.output_dir:
        write_outputs(run, Path(args.output_dir).resolve())
    else:
        default_output_dir = project_root / "expected" / "generated"
        write_outputs(run, default_output_dir)
    print("Generated deliverables for", run.project.project_id)


if __name__ == "__main__":
    main()
