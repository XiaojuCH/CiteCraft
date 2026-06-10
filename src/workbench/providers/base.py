"""Narrow provider seam for generation tasks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ProviderConfig:
    name: str
    model: str = ""
    api_key: str = ""
    base_url: str = ""
    timeout_seconds: int = 20
    max_output_chars: int = 900
    fallback_on_error: bool = True
    metadata: Optional[Dict[str, str]] = None


class GenerationProvider(ABC):
    """A tiny text-generation seam for deliverable drafting."""

    name = "base"

    def __init__(self, config: ProviderConfig = None):
        self.config = config or ProviderConfig(name=self.name)

    @abstractmethod
    def compose(self, task: str, seed_text: str, metadata: Dict[str, str]) -> str:
        """Return user-facing text for one deliverable node."""
