"""Base source adapter helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from workbench.contracts.evidence import Locator
from workbench.contracts.sources import SourceChunk, SourceDocument


@dataclass
class NormalizedSegment:
    text: str
    locator: Locator
    section: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


class SourceAdapter:
    source_type = "base"

    def load(self, source_input, project_config) -> SourceDocument:
        raise NotImplementedError


def build_document(
    source_id: str,
    source_type: str,
    label: str,
    content: str,
    root_locator: Locator,
    segments: Iterable[NormalizedSegment],
    metadata: Optional[Dict[str, str]] = None,
) -> SourceDocument:
    metadata = metadata or {}
    chunks: List[SourceChunk] = []
    for index, segment in enumerate(segments, start=1):
        chunk_id = f"{source_id}-chunk-{index:03d}"
        chunk_metadata = dict(segment.metadata)
        chunk_metadata["source_type"] = source_type
        chunks.append(
            SourceChunk(
                source_id=source_id,
                chunk_id=chunk_id,
                text=segment.text,
                locator=segment.locator,
                section=segment.section,
                metadata=chunk_metadata,
            )
        )
    return SourceDocument(
        source_id=source_id,
        source_type=source_type,
        label=label,
        content=content,
        chunks=chunks,
        locator=root_locator,
        metadata=metadata,
    )

