from pathlib import Path

from workbench.deliverables.registry import generate_deliverables
from workbench.evidence.index import EvidenceIndex
from workbench.pipeline.run import run_project
from workbench.sources.registry import load_documents
from workbench.contracts.project import load_project_config
from workbench.providers.base import GenerationProvider


PROJECT_ROOT = Path(__file__).resolve().parents[1] / "examples" / "academia" / "demo-01"


class PrefixProvider(GenerationProvider):
    name = "prefix"

    def compose(self, task: str, seed_text: str, metadata):
        return "[%s] %s" % (task, seed_text)


def test_pipeline_defaults_to_deterministic_provider():
    run = run_project(PROJECT_ROOT)
    assert run.provider_name == "deterministic"


def test_custom_provider_can_shape_deliverable_text():
    project = load_project_config(PROJECT_ROOT)
    documents = load_documents(project)
    evidence_index = EvidenceIndex(documents)
    deliverables = generate_deliverables(project, documents, evidence_index, PrefixProvider())
    assert deliverables["brief"].sections[0].items[0].text.startswith("[brief.summary]")
    assert deliverables["literature_matrix"].cells[0].value.startswith("[literature_matrix.cell]")
    assert deliverables["slides"].slides[0].bullets[0].text.startswith("[slides.bullet]")
