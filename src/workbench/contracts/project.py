"""Project contract and loader."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml


@dataclass
class SourceInput:
    source_id: str
    type: str
    label: str
    path: Optional[str] = None
    url: Optional[str] = None
    cache_path: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProjectConfig:
    project_root: Path
    project_id: str
    title: str
    audience: str
    positioning: str
    requested_deliverables: List[str]
    demo_order: List[str]
    comparison_dimensions: List[str]
    brief_focus: str
    slide_goal: str
    sources: List[SourceInput]
    metadata: Dict[str, str] = field(default_factory=dict)

    def resolve_path(self, value: str) -> Path:
        return (self.project_root / value).resolve()


def load_project_config(project_root: Path) -> ProjectConfig:
    payload = yaml.safe_load((project_root / "project.yaml").read_text(encoding="utf-8"))
    sources = [SourceInput(**item) for item in payload["sources"]]
    return ProjectConfig(
        project_root=project_root.resolve(),
        project_id=payload["project_id"],
        title=payload["title"],
        audience=payload["audience"],
        positioning=payload["positioning"],
        requested_deliverables=payload["requested_deliverables"],
        demo_order=payload["demo_order"],
        comparison_dimensions=payload["comparison_dimensions"],
        brief_focus=payload["brief_focus"],
        slide_goal=payload["slide_goal"],
        sources=sources,
        metadata=payload.get("metadata", {}),
    )

