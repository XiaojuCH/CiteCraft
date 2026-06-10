"""Lightweight evidence indexing and retrieval."""

from __future__ import annotations

import re
from typing import Iterable, List, Sequence

from workbench.contracts.sources import SourceChunk, SourceDocument


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class EvidenceIndex:
    def __init__(self, documents: Sequence[SourceDocument]):
        self.documents = list(documents)
        self.chunks: List[SourceChunk] = []
        for document in self.documents:
            self.chunks.extend(document.chunks)

    def pick(
        self,
        query: str,
        limit: int = 1,
        source_id: str = None,
        preferred_types: Iterable[str] = (),
        require_keyword: bool = False,
    ) -> List[SourceChunk]:
        query_terms = tokenize(query)
        preferred_types = list(preferred_types)
        ranked = []
        for chunk in self.chunks:
            if source_id and chunk.source_id != source_id:
                continue
            haystack = " ".join(
                [
                    chunk.text,
                    chunk.section or "",
                    chunk.metadata.get("source_type", ""),
                ]
            ).lower()
            overlap = sum(1 for term in query_terms if term in haystack)
            if require_keyword and overlap == 0:
                continue
            type_bonus = 2 if chunk.metadata.get("source_type") in preferred_types else 0
            title_bonus = 1 if chunk.section and any(term in chunk.section.lower() for term in query_terms) else 0
            score = overlap + type_bonus + title_bonus
            if score > 0 or not require_keyword:
                ranked.append((score, len(chunk.text), chunk))
        ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [item[2] for item in ranked[:limit]]

