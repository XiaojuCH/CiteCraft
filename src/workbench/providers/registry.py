"""Provider registry."""

from __future__ import annotations

from typing import Dict

from workbench.providers.deterministic import DeterministicProvider


PROVIDERS = {
    "deterministic": DeterministicProvider,
}


def get_provider(name: str = "deterministic"):
    provider_cls = PROVIDERS.get(name)
    if provider_cls is None:
        raise KeyError("Unknown provider: %s" % name)
    return provider_cls()
