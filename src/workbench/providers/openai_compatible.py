"""OpenAI-compatible provider with safe deterministic fallback."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Dict

from workbench.providers.base import GenerationProvider, ProviderConfig


class OpenAICompatibleProvider(GenerationProvider):
    """Call an OpenAI-compatible chat completions endpoint.

    The provider is intentionally narrow. It rewrites one node at a time from
    already-selected evidence text, and falls back to the seed text when config
    is missing or the request fails.
    """

    name = "openai-compatible"

    def __init__(self, config: ProviderConfig = None):
        super().__init__(config)
        if not self.config.base_url:
            self.config.base_url = "https://api.openai.com/v1"
        if not self.config.model:
            self.config.model = "gpt-4.1-mini"

    def compose(self, task: str, seed_text: str, metadata: Dict[str, str]) -> str:
        if not self.config.api_key:
            return seed_text
        try:
            rewritten = self._call_model(task, seed_text, metadata)
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, KeyError):
            if self.config.fallback_on_error:
                return seed_text
            raise
        return rewritten[: self.config.max_output_chars].strip() or seed_text

    def _call_model(self, task: str, seed_text: str, metadata: Dict[str, str]) -> str:
        url = self.config.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.config.model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You rewrite evidence-backed deliverable nodes. "
                        "Keep the meaning faithful to the seed evidence. "
                        "Do not invent facts, sources, or citations. "
                        "Return only the final node text."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "task": task,
                            "metadata": metadata,
                            "seed_text": seed_text,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer %s" % self.config.api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
