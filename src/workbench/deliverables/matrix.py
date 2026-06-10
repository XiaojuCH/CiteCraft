"""Deterministic literature matrix generator."""

from __future__ import annotations

from typing import List

from workbench.contracts.deliverables import (
    LiteratureMatrixDeliverable,
    MatrixCell,
    MatrixColumn,
    MatrixRow,
    RenderHints,
    TraceableTextNode,
)
from workbench.evidence.binder import make_trace
from workbench.ingest.normalize import sentence_snippet


def _dimension_query(label: str) -> str:
    lowered = label.lower()
    if "claim" in lowered or "question" in lowered:
        return "claim finding summary traceability reviewable"
    if "evidence" in lowered or "method" in lowered:
        return "practical guidance evidence method workflow deterministic pipeline source chunks"
    if "relevance" in lowered or "deliverable" in lowered:
        return "deliverable brief slides matrix presenter demo reuse"
    if "limit" in lowered or "risk" in lowered:
        return "limitation risk caution fidelity human judgment pptx"
    return lowered


def generate_matrix(project_config, documents, evidence_index, provider) -> LiteratureMatrixDeliverable:
    source_ids = [document.source_id for document in documents]
    columns = [MatrixColumn(column_id="matrix.col.%02d" % index, label=label) for index, label in enumerate(project_config.comparison_dimensions, start=1)]
    rows = [MatrixRow(row_id="matrix.row.%02d" % index, source_id=document.source_id, label=document.label) for index, document in enumerate(documents, start=1)]

    cells: List[MatrixCell] = []
    for row in rows:
        for column in columns:
            query = _dimension_query(column.label)
            chunk = evidence_index.pick(query, limit=1, source_id=row.source_id, require_keyword=False)[0]
            lowered = column.label.lower()
            is_factual = not any(term in lowered for term in ["takeaway", "recommendation", "narrative"])
            traces = [make_trace(chunk, "trc_%s_%s" % (row.row_id.replace(".", "_"), column.column_id.replace(".", "_")))] if is_factual else []
            cells.append(
                MatrixCell(
                    node_id="matrix.cell.row%s.col%s" % (row.row_id.split(".")[-1], column.column_id.split(".")[-1]),
                    row_id=row.row_id,
                    column_id=column.column_id,
                    value=provider.compose(
                        task="literature_matrix.cell",
                        seed_text=sentence_snippet(chunk.text, limit=120),
                        metadata={
                            "column": column.label,
                            "row_label": row.label,
                            "source_id": row.source_id,
                            "is_factual": "true" if is_factual else "false",
                        },
                    ),
                    is_factual=is_factual,
                    trace_refs=traces,
                )
            )

    synthesis = [
        TraceableTextNode(
            node_id="matrix.synthesis.01",
            kind="synthesis",
            title="Common thread",
            text=provider.compose(
                task="literature_matrix.synthesis",
                seed_text="All three sources treat traceability as the trust lever that turns raw material into reusable outputs.",
                metadata={"theme": "traceability"},
            ),
            trace_refs=[
                make_trace(evidence_index.pick("trace panel claim source chunk traceability reviewable", preferred_types=["url", "pdf"], limit=1)[0], "trc_matrix_synth_01"),
            ],
        ),
        TraceableTextNode(
            node_id="matrix.synthesis.02",
            kind="synthesis",
            title="Delivery bias",
            text=provider.compose(
                task="literature_matrix.synthesis",
                seed_text="Slides stay in P0 because visible, content-first deliverables are easier to demo than perfect export fidelity.",
                metadata={"theme": "slides"},
            ),
            trace_refs=[
                make_trace(evidence_index.pick("slides demo content first pptx wait speaker notes fidelity", preferred_types=["url", "folder"], limit=1)[0], "trc_matrix_synth_02"),
            ],
        ),
    ]

    return LiteratureMatrixDeliverable(
        deliverable_id="matrix-demo-01",
        deliverable_type="literature_matrix",
        version="0.1",
        project_id=project_config.project_id,
        title="Literature Matrix",
        source_ids=source_ids,
        columns=columns,
        rows=rows,
        cells=cells,
        synthesis=synthesis,
        render_hints=RenderHints(extras={"compactness": "comfortable", "show_source_column": "true"}),
    )
