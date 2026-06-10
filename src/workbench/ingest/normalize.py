"""Text normalization helpers for source ingestion."""

from __future__ import annotations

import re
from typing import List


def clean_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def split_paragraphs(text: str) -> List[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return [block.strip() for block in cleaned.split("\n\n") if block.strip()]


def strip_markdown(text: str) -> str:
    stripped = re.sub(r"^#{1,6}\s*", "", text.strip())
    stripped = re.sub(r"^\-\s*", "", stripped)
    stripped = re.sub(r"\*\*(.*?)\*\*", r"\1", stripped)
    stripped = re.sub(r"`([^`]+)`", r"\1", stripped)
    return stripped.strip()


def sentence_snippet(text: str, limit: int = 200) -> str:
    stripped = strip_markdown(clean_text(text))
    if len(stripped) <= limit:
        return stripped
    return stripped[: limit - 3].rstrip() + "..."

