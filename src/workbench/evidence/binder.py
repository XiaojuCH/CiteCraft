"""Trace attachment helpers."""

from __future__ import annotations

from workbench.contracts.evidence import TraceAttachment
from workbench.contracts.sources import SourceChunk
from workbench.ingest.normalize import sentence_snippet


def make_trace(chunk: SourceChunk, trace_id: str, relation: str = "supports") -> TraceAttachment:
    return TraceAttachment(
        trace_id=trace_id,
        source_id=chunk.source_id,
        chunk_id=chunk.chunk_id,
        relation=relation,
        locator=chunk.locator,
        snippet=sentence_snippet(chunk.text, limit=180),
    )

