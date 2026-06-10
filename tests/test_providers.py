from pathlib import Path
import json

from workbench.deliverables.registry import generate_deliverables
from workbench.evidence.index import EvidenceIndex
from workbench.pipeline.run import run_project
from workbench.sources.registry import load_documents
from workbench.contracts.project import load_project_config
from workbench.providers.base import GenerationProvider, ProviderConfig
from workbench.providers.openai_compatible import OpenAICompatibleProvider
from workbench.providers.registry import get_provider


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


def test_openai_compatible_provider_falls_back_without_api_key():
    provider = OpenAICompatibleProvider(ProviderConfig(name="openai-compatible"))
    assert provider.compose("brief.summary", "Seed text", {}) == "Seed text"


def test_registry_builds_openai_compatible_provider_from_env(monkeypatch):
    monkeypatch.setenv("WORKBENCH_MODEL", "example-model")
    monkeypatch.setenv("WORKBENCH_API_KEY", "example-key")
    monkeypatch.setenv("WORKBENCH_BASE_URL", "https://example.test/v1")
    provider = get_provider("openai-compatible")
    assert provider.config.model == "example-model"
    assert provider.config.api_key == "example-key"
    assert provider.config.base_url == "https://example.test/v1"


def test_openai_compatible_provider_uses_model_response(monkeypatch):
    provider = OpenAICompatibleProvider(
        ProviderConfig(
            name="openai-compatible",
            api_key="example-key",
            model="example-model",
            base_url="https://example.test/v1",
        )
    )

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(
                {
                    "choices": [
                        {
                            "message": {
                                "content": "Polished output",
                            }
                        }
                    ]
                }
            ).encode("utf-8")

    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout=0: FakeResponse())
    assert provider.compose("brief.summary", "Seed text", {"objective": "demo"}) == "Polished output"
