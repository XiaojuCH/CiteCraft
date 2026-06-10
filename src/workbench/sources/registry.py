"""Source adapter registry."""

from __future__ import annotations

from typing import Dict, List

from workbench.sources.folder import FolderSourceAdapter
from workbench.sources.pdf import PdfSourceAdapter
from workbench.sources.url import UrlSourceAdapter


ADAPTERS = {
    "pdf": PdfSourceAdapter(),
    "url": UrlSourceAdapter(),
    "folder": FolderSourceAdapter(),
}


def load_documents(project_config) -> List:
    documents = []
    for source_input in project_config.sources:
        adapter = ADAPTERS[source_input.type]
        documents.append(adapter.load(source_input, project_config))
    return documents

