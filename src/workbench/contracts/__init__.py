"""Structured contracts for sources, evidence, and deliverables."""

from .deliverables import (
    BriefDeliverable,
    LiteratureMatrixDeliverable,
    SlidesDeliverable,
)
from .evidence import Locator, TraceAttachment
from .project import ProjectConfig, SourceInput
from .sources import SourceChunk, SourceDocument

__all__ = [
    "BriefDeliverable",
    "LiteratureMatrixDeliverable",
    "Locator",
    "ProjectConfig",
    "SlidesDeliverable",
    "SourceChunk",
    "SourceDocument",
    "SourceInput",
    "TraceAttachment",
]

