"""Folder adapter for markdown and text notes."""

from __future__ import annotations

from pathlib import Path
from typing import List

from workbench.contracts.evidence import Locator
from workbench.ingest.normalize import split_paragraphs
from workbench.sources.base import NormalizedSegment, SourceAdapter, build_document


class FolderSourceAdapter(SourceAdapter):
    source_type = "folder"

    def load(self, source_input, project_config):
        path = project_config.resolve_path(source_input.path)
        content_parts: List[str] = []
        segments: List[NormalizedSegment] = []
        for file_path in sorted(path.rglob("*")):
            if not file_path.is_file() or file_path.suffix.lower() not in {".md", ".txt"}:
                continue
            relative = file_path.relative_to(path).as_posix()
            text = file_path.read_text(encoding="utf-8")
            content_parts.append("## " + relative + "\n" + text.strip())
            current_section = relative
            for block in split_paragraphs(text):
                if block.startswith("#"):
                    current_section = block.lstrip("# ").strip()
                segments.append(
                    NormalizedSegment(
                        text=block,
                        section=current_section,
                        locator=Locator(
                            label=relative,
                            filepath=str(file_path),
                            section=current_section,
                        ),
                    )
                )
        return build_document(
            source_id=source_input.source_id,
            source_type=self.source_type,
            label=source_input.label,
            content="\n\n".join(content_parts),
            root_locator=Locator(label=path.name, filepath=str(path)),
            segments=segments,
            metadata={"path": str(path)},
        )

