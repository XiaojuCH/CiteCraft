"""Evidence and trace contracts."""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Locator:
    label: str
    page: Optional[int] = None
    section: Optional[str] = None
    filepath: Optional[str] = None
    url: Optional[str] = None


@dataclass
class TraceAttachment:
    trace_id: str
    source_id: str
    chunk_id: str
    relation: str
    locator: Locator
    snippet: str
    metadata: Dict[str, str] = field(default_factory=dict)

