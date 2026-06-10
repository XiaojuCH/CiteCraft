"""Deterministic slides generator."""

from __future__ import annotations

from typing import List

from workbench.contracts.deliverables import (
    BriefDeliverable,
    LiteratureMatrixDeliverable,
    RenderHints,
    Slide,
    SlideBullet,
    SlideNote,
    SlideOutlineItem,
    SlidesDeliverable,
)


def _bullet(provider, node_id: str, kind: str, text: str, metadata, trace_refs=None) -> SlideBullet:
    return SlideBullet(
        node_id=node_id,
        kind=kind,
        text=provider.compose(task="slides.bullet", seed_text=text, metadata=metadata),
        trace_refs=trace_refs or [],
    )


def _note(provider, node_id: str, text: str, metadata, trace_refs=None) -> SlideNote:
    return SlideNote(
        node_id=node_id,
        text=provider.compose(task="slides.note", seed_text=text, metadata=metadata),
        trace_refs=trace_refs or [],
    )


def generate_slides(project_config, documents, brief: BriefDeliverable, matrix: LiteratureMatrixDeliverable, provider) -> SlidesDeliverable:
    source_ids = [document.source_id for document in documents]
    outline = [
        SlideOutlineItem(node_id="slides.outline.01", title="Framing", purpose="Set up the journal club objective."),
        SlideOutlineItem(node_id="slides.outline.02", title="Why traceability matters", purpose="Show why cited deliverables build trust."),
        SlideOutlineItem(node_id="slides.outline.03", title="What the sources say", purpose="Summarize cross-source findings."),
        SlideOutlineItem(node_id="slides.outline.04", title="Recommended demo shape", purpose="Translate findings into a visible product path."),
        SlideOutlineItem(node_id="slides.outline.05", title="Open questions", purpose="Leave the audience with next steps."),
    ]

    finding_a = brief.sections[1].items[0]
    finding_b = brief.sections[1].items[1]
    finding_c = brief.sections[1].items[2]
    limitation = brief.sections[2].items[0]
    question = brief.sections[3].items[0]
    synthesis = matrix.synthesis[0]

    slides: List[Slide] = [
        Slide(
            node_id="slides.slide.01",
            slide_number=1,
            title="Journal Club Framing",
            bullets=[
                _bullet(provider, "slides.slide.01.bullet.01", "context", project_config.slide_goal, {"slide": "1", "kind": "context"}),
                _bullet(provider, "slides.slide.01.bullet.02", "claim", brief.sections[0].items[0].text, {"slide": "1", "kind": "claim"}, brief.sections[0].items[0].trace_refs),
            ],
            speaker_notes=[
                _note(provider, "slides.slide.01.note.01", "Open by anchoring on the audience and the promised output shape.", {"slide": "1"}),
            ],
            render_hints={"layout": "title-plus-bullets"},
        ),
        Slide(
            node_id="slides.slide.02",
            slide_number=2,
            title="Why Traceability Matters",
            bullets=[
                _bullet(provider, "slides.slide.02.bullet.01", "claim", finding_a.text, {"slide": "2", "kind": "claim"}, finding_a.trace_refs),
                _bullet(provider, "slides.slide.02.bullet.02", "claim", finding_b.text, {"slide": "2", "kind": "claim"}, finding_b.trace_refs),
            ],
            speaker_notes=[
                _note(provider, "slides.slide.02.note.01", "Explain that visible trace links reduce the leap of faith in AI-generated outputs.", {"slide": "2"}),
            ],
            render_hints={"layout": "two-point"},
        ),
        Slide(
            node_id="slides.slide.03",
            slide_number=3,
            title="Cross-Source Takeaways",
            bullets=[
                _bullet(provider, "slides.slide.03.bullet.01", "claim", synthesis.text, {"slide": "3", "kind": "claim"}, synthesis.trace_refs),
                _bullet(provider, "slides.slide.03.bullet.02", "claim", finding_c.text, {"slide": "3", "kind": "claim"}, finding_c.trace_refs),
            ],
            speaker_notes=[
                _note(provider, "slides.slide.03.note.01", "Use the matrix view as the bridge between reading and presenting.", {"slide": "3"}),
            ],
            render_hints={"layout": "takeaways"},
        ),
        Slide(
            node_id="slides.slide.04",
            slide_number=4,
            title="Recommended Demo Shape",
            bullets=[
                _bullet(provider, "slides.slide.04.bullet.01", "recommendation", "Keep the pipeline deterministic in P0: ingest, chunk, extract evidence, generate, bind, render.", {"slide": "4", "kind": "recommendation"}),
                _bullet(provider, "slides.slide.04.bullet.02", "claim", limitation.text, {"slide": "4", "kind": "claim"}, limitation.trace_refs),
            ],
            speaker_notes=[
                _note(provider, "slides.slide.04.note.01", "Stress that content quality and trace clarity matter more than export polish in the first demo.", {"slide": "4"}),
            ],
            render_hints={"layout": "recommendation"},
        ),
        Slide(
            node_id="slides.slide.05",
            slide_number=5,
            title="Open Questions",
            bullets=[
                _bullet(provider, "slides.slide.05.bullet.01", "question", question.text, {"slide": "5", "kind": "question"}, question.trace_refs),
                _bullet(provider, "slides.slide.05.bullet.02", "question", "What is the minimum template system needed before opening plugin and skill extension points?", {"slide": "5", "kind": "question"}),
            ],
            speaker_notes=[
                _note(provider, "slides.slide.05.note.01", "End by inviting discussion on expansion beyond academia without weakening the initial wedge.", {"slide": "5"}),
            ],
            render_hints={"layout": "closing"},
        ),
    ]

    return SlidesDeliverable(
        deliverable_id="slides-demo-01",
        deliverable_type="slides",
        version="0.1",
        project_id=project_config.project_id,
        title="Journal Club Slide Plan",
        deck_goal=project_config.slide_goal,
        source_ids=source_ids,
        outline=outline,
        slides=slides,
        render_hints=RenderHints(extras={"theme": "clean", "aspect_ratio": "16:9", "show_notes": "true"}),
    )
