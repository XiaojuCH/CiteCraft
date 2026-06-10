"""Deliverable registry and generation entrypoint."""

from __future__ import annotations

from workbench.deliverables.brief import generate_brief
from workbench.deliverables.matrix import generate_matrix
from workbench.deliverables.slides import generate_slides


def generate_deliverables(project_config, documents, evidence_index, provider):
    brief = generate_brief(project_config, documents, evidence_index, provider)
    matrix = generate_matrix(project_config, documents, evidence_index, provider)
    slides = generate_slides(project_config, documents, brief, matrix, provider)
    return {
        "brief": brief,
        "literature_matrix": matrix,
        "slides": slides,
    }
