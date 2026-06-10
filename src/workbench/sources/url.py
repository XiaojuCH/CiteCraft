"""URL adapter with deterministic cache fallback for the demo path."""

from __future__ import annotations

from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

from workbench.contracts.evidence import Locator
from workbench.ingest.normalize import clean_text, split_paragraphs
from workbench.sources.base import NormalizedSegment, SourceAdapter, build_document


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return clean_text(soup.get_text("\n"))


def _load_url_text(url: str, cache_path: Path = None) -> str:
    if cache_path and cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    if "<html" in response.text.lower():
        return _html_to_text(response.text)
    return clean_text(response.text)


class UrlSourceAdapter(SourceAdapter):
    source_type = "url"

    def load(self, source_input, project_config):
        cache_path = project_config.resolve_path(source_input.cache_path) if source_input.cache_path else None
        text = _load_url_text(source_input.url, cache_path=cache_path)
        blocks = split_paragraphs(text)
        locator = Locator(label=source_input.url, url=source_input.url, filepath=str(cache_path) if cache_path else None)
        segments: List[NormalizedSegment] = []
        current_section = "URL"
        for block in blocks:
            if block.startswith("#"):
                current_section = block.lstrip("# ").strip()
            segments.append(
                NormalizedSegment(
                    text=block,
                    section=current_section,
                    locator=Locator(
                        label=current_section if current_section != "URL" else source_input.url,
                        section=current_section,
                        url=source_input.url,
                        filepath=str(cache_path) if cache_path else None,
                    ),
                )
            )
        return build_document(
            source_id=source_input.source_id,
            source_type=self.source_type,
            label=source_input.label,
            content=text,
            root_locator=locator,
            segments=segments,
            metadata={"url": source_input.url, "cache_path": str(cache_path) if cache_path else ""},
        )

