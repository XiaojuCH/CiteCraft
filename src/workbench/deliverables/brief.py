"""Deterministic cited brief generator."""

from __future__ import annotations

from typing import Dict, List

from workbench.contracts.deliverables import BriefDeliverable, BriefSection, RenderHints, TraceableTextNode
from workbench.evidence.binder import make_trace
from workbench.ingest.normalize import sentence_snippet


def _node(node_id: str, kind: str, text: str, title: str = "", traces=None) -> TraceableTextNode:
    return TraceableTextNode(node_id=node_id, kind=kind, title=title, text=text, trace_refs=traces or [])


def _compose(provider, task: str, seed_text: str, metadata: Dict[str, str]) -> str:
    return provider.compose(task=task, seed_text=seed_text, metadata=metadata)


def generate_brief(project_config, documents, evidence_index, provider) -> BriefDeliverable:
    source_ids = [document.source_id for document in documents]
    summary_chunk = evidence_index.pick(project_config.brief_focus + " objective framing", limit=1, preferred_types=["folder", "url"])[0]
    finding_chunks = evidence_index.pick(
        "finding deliverable trace slides brief matrix deterministic trust reviewable",
        limit=3,
        preferred_types=["pdf", "url"],
    )
    limitation_chunks = evidence_index.pick("limitation risk caution trade-off trust fidelity", limit=2, preferred_types=["pdf", "url", "folder"])
    question_chunks = evidence_index.pick("question next step open issue presenter follow-up", limit=2, preferred_types=["folder"], require_keyword=False)

    summary = BriefSection(
        node_id="brief.section.summary",
        title="Summary",
        items=[
            _node(
                node_id="brief.summary.01",
                kind="summary",
                text=_compose(
                    provider,
                    task="brief.summary",
                    seed_text=sentence_snippet(summary_chunk.text, limit=220),
                    metadata={"objective": project_config.brief_focus, "source_id": summary_chunk.source_id},
                ),
                traces=[make_trace(summary_chunk, "trc_brief_summary_01")],
            )
        ],
    )

    findings: List[TraceableTextNode] = []
    for index, chunk in enumerate(finding_chunks, start=1):
        findings.append(
            _node(
                node_id="brief.finding.%02d" % index,
                kind="finding",
                title="Key finding %d" % index,
                text=_compose(
                    provider,
                    task="brief.finding",
                    seed_text=sentence_snippet(chunk.text, limit=220),
                    metadata={"objective": project_config.brief_focus, "source_id": chunk.source_id, "rank": str(index)},
                ),
                traces=[make_trace(chunk, "trc_brief_finding_%02d" % index)],
            )
        )

    limitations: List[TraceableTextNode] = []
    for index, chunk in enumerate(limitation_chunks, start=1):
        limitations.append(
            _node(
                node_id="brief.limitation.%02d" % index,
                kind="limitation",
                text=_compose(
                    provider,
                    task="brief.limitation",
                    seed_text=sentence_snippet(chunk.text, limit=220),
                    metadata={"objective": project_config.brief_focus, "source_id": chunk.source_id, "rank": str(index)},
                ),
                traces=[make_trace(chunk, "trc_brief_limitation_%02d" % index)],
            )
        )

    questions: List[TraceableTextNode] = []
    for index, chunk in enumerate(question_chunks, start=1):
        questions.append(
            _node(
                node_id="brief.question.%02d" % index,
                kind="question",
                text=_compose(
                    provider,
                    task="brief.question",
                    seed_text=sentence_snippet(chunk.text, limit=220),
                    metadata={"objective": project_config.brief_focus, "source_id": chunk.source_id, "rank": str(index)},
                ),
                traces=[make_trace(chunk, "trc_brief_question_%02d" % index)],
            )
        )

    sections = [
        summary,
        BriefSection(node_id="brief.section.key_findings", title="Key Findings", items=findings),
        BriefSection(node_id="brief.section.limitations", title="Limitations", items=limitations),
        BriefSection(node_id="brief.section.open_questions", title="Open Questions", items=questions),
    ]
    return BriefDeliverable(
        deliverable_id="brief-demo-01",
        deliverable_type="brief",
        version="0.1",
        project_id=project_config.project_id,
        title="Cited Brief",
        objective=project_config.brief_focus,
        source_ids=source_ids,
        sections=sections,
        render_hints=RenderHints(extras={"show_trace_badges": "true", "section_order": "summary,key_findings,limitations,open_questions"}),
    )
