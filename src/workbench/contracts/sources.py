"""Normalized source contracts."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .evidence import Locator


@dataclass
class SourceChunk:
    source_id: str
    chunk_id: str
    text: str
    locator: Locator
    section: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class SourceDocument:
    source_id: str
    source_type: str
    label: str
    content: str
    chunks: List[SourceChunk]
    locator: Locator
    metadata: Dict[str, str] = field(default_factory=dict)

