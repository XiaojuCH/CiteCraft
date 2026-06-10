"""Very small PDF adapter for demo-friendly, text-based PDFs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List

from workbench.contracts.evidence import Locator
from workbench.ingest.normalize import clean_text
from workbench.sources.base import NormalizedSegment, SourceAdapter, build_document


def _decode_pdf_text(token: str) -> str:
    token = token.replace(r"\(", "(").replace(r"\)", ")").replace(r"\n", "\n").replace(r"\t", "\t")
    token = token.replace(r"\\", "\\")
    return token


def extract_text_from_minimal_pdf(path: Path) -> str:
    payload = path.read_bytes().decode("latin-1", errors="ignore")
    tj_matches = re.findall(r"\((.*?)\)\s*Tj", payload, flags=re.DOTALL)
    tj_array_matches = re.findall(r"\[(.*?)\]\s*TJ", payload, flags=re.DOTALL)
    lines: List[str] = []
    for match in tj_matches:
        text = clean_text(_decode_pdf_text(match))
        if text:
            lines.append(text)
    for match in tj_array_matches:
        strings = re.findall(r"\((.*?)\)", match, flags=re.DOTALL)
        text = clean_text(" ".join(_decode_pdf_text(item) for item in strings))
        if text:
            lines.append(text)
    return "\n".join(lines)


class PdfSourceAdapter(SourceAdapter):
    source_type = "pdf"

    def load(self, source_input, project_config):
        path = project_config.resolve_path(source_input.path)
        text = extract_text_from_minimal_pdf(path)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        filename = path.name
        segments = []
        for line in lines:
            section = line.split(":", 1)[0] if ":" in line else "PDF"
            segments.append(
                NormalizedSegment(
                    text=line,
                    section=section,
                    locator=Locator(label=f"{filename} p.1", page=1, filepath=str(path)),
                )
            )
        return build_document(
            source_id=source_input.source_id,
            source_type=self.source_type,
            label=source_input.label,
            content=text,
            root_locator=Locator(label=filename, filepath=str(path), page=1),
            segments=segments,
            metadata={"path": str(path)},
        )

