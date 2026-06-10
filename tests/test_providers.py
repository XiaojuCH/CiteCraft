from pathlib import Path
import json

from workbench.deliverables.registry import generate_deliverables
from workbench.evidence.index import EvidenceIndex
from workbench.pipeline.run import run_project
from workbench.sources.registry import load_documents
from workbench.contracts.project import load_project_config
from workbench.providers.base import GenerationProvider, ProviderConfig
from workbench.providers.openai_compatible import OpenAICompatibleProvider
from workbench.providers.prompt_recipes import build_messages, get_prompt_recipe
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


def test_prompt_recipes_are_task_specific():
    brief_recipe = get_prompt_recipe("brief.finding")
    slide_recipe = get_prompt_recipe("slides.bullet")
    assert "key finding" in brief_recipe.system_goal.lower()
    assert "slide bullet" in slide_recipe.system_goal.lower()


def test_openai_payload_uses_task_specific_messages():
    provider = OpenAICompatibleProvider(
        ProviderConfig(
            name="openai-compatible",
            api_key="example-key",
            model="example-model",
            base_url="https://example.test/v1",
        )
    )
    payload = provider.build_payload("slides.bullet", "Seed bullet", {"slide": "2", "kind": "claim"})
    system_message = payload["messages"][0]["content"]
    user_message = payload["messages"][1]["content"]
    assert "presentation slide" in system_message.lower()
    assert '"slide": "2"' in user_message


def test_build_messages_include_seed_text_and_metadata():
    messages = build_messages("literature_matrix.cell", "Seed cell", {"column": "Evidence or method"})
    assert messages[1]["content"].count("Seed cell") == 1
    assert '"column": "Evidence or method"' in messages[1]["content"]
