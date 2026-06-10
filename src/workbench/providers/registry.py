"""Provider registry."""

from __future__ import annotations

import os

from workbench.providers.base import ProviderConfig
from workbench.providers.deterministic import DeterministicProvider
from workbench.providers.openai_compatible import OpenAICompatibleProvider


PROVIDERS = {
    "deterministic": DeterministicProvider,
    "openai-compatible": OpenAICompatibleProvider,
}


def get_provider(name: str = "deterministic"):
    provider_cls = PROVIDERS.get(name)
    if provider_cls is None:
        raise KeyError("Unknown provider: %s" % name)
    config = ProviderConfig(
        name=name,
        model=os.environ.get("WORKBENCH_MODEL", ""),
        api_key=os.environ.get("WORKBENCH_API_KEY", ""),
        base_url=os.environ.get("WORKBENCH_BASE_URL", ""),
        timeout_seconds=int(os.environ.get("WORKBENCH_PROVIDER_TIMEOUT", "20")),
        max_output_chars=int(os.environ.get("WORKBENCH_MAX_OUTPUT_CHARS", "900")),
        fallback_on_error=os.environ.get("WORKBENCH_FALLBACK_ON_ERROR", "1") != "0",
    )
    return provider_cls(config)
