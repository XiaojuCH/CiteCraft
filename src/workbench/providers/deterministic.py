"""Default provider that preserves the deterministic P0 behavior."""

from __future__ import annotations

from typing import Dict

from workbench.providers.base import GenerationProvider


class DeterministicProvider(GenerationProvider):
    name = "deterministic"

    def compose(self, task: str, seed_text: str, metadata: Dict[str, str]) -> str:
        return seed_text

