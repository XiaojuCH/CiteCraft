"""Structured deliverable contracts."""

from dataclasses import dataclass, field
from typing import Dict, List

from .evidence import TraceAttachment


@dataclass
class RenderHints:
    tone: str = "professional"
    citation_mode: str = "inline_badge"
    audience_style: str = "academia"
    density: str = "medium"
    extras: Dict[str, str] = field(default_factory=dict)


@dataclass
class TraceableTextNode:
    node_id: str
    text: str
    trace_refs: List[TraceAttachment] = field(default_factory=list)
    kind: str = "text"
    title: str = ""


@dataclass
class BriefSection:
    node_id: str
    title: str
    items: List[TraceableTextNode] = field(default_factory=list)


@dataclass
class BriefDeliverable:
    deliverable_id: str
    deliverable_type: str
    version: str
    project_id: str
    title: str
    objective: str
    source_ids: List[str]
    sections: List[BriefSection]
    render_hints: RenderHints


@dataclass
class MatrixColumn:
    column_id: str
    label: str


@dataclass
class MatrixRow:
    row_id: str
    source_id: str
    label: str


@dataclass
class MatrixCell:
    node_id: str
    row_id: str
    column_id: str
    value: str
    is_factual: bool = True
    trace_refs: List[TraceAttachment] = field(default_factory=list)


@dataclass
class LiteratureMatrixDeliverable:
    deliverable_id: str
    deliverable_type: str
    version: str
    project_id: str
    title: str
    source_ids: List[str]
    columns: List[MatrixColumn]
    rows: List[MatrixRow]
    cells: List[MatrixCell]
    synthesis: List[TraceableTextNode]
    render_hints: RenderHints


@dataclass
class SlideOutlineItem:
    node_id: str
    title: str
    purpose: str


@dataclass
class SlideBullet:
    node_id: str
    kind: str
    text: str
    trace_refs: List[TraceAttachment] = field(default_factory=list)


@dataclass
class SlideNote:
    node_id: str
    text: str
    trace_refs: List[TraceAttachment] = field(default_factory=list)


@dataclass
class Slide:
    node_id: str
    slide_number: int
    title: str
    bullets: List[SlideBullet]
    speaker_notes: List[SlideNote]
    render_hints: Dict[str, str] = field(default_factory=dict)


@dataclass
class SlidesDeliverable:
    deliverable_id: str
    deliverable_type: str
    version: str
    project_id: str
    title: str
    deck_goal: str
    source_ids: List[str]
    outline: List[SlideOutlineItem]
    slides: List[Slide]
    render_hints: RenderHints
