"""Narrow provider seam for generation tasks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class GenerationProvider(ABC):
    """A tiny text-generation seam for deliverable drafting."""

    name = "base"

    @abstractmethod
    def compose(self, task: str, seed_text: str, metadata: Dict[str, str]) -> str:
        """Return user-facing text for one deliverable node."""

