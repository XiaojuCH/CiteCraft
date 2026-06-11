from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "citecraft-multi-agent"
AGENT_DIR = ROOT / ".codex" / "agents"


def test_repo_skill_exists_and_has_no_todos():
    skill_md = SKILL_DIR / "SKILL.md"
    assert skill_md.exists()
    text = skill_md.read_text(encoding="utf-8")
    assert "[TODO:" not in text
    assert "Coordinate repo-scoped subagents" in text


def test_repo_skill_frontmatter_and_openai_yaml_are_valid():
    skill_md = SKILL_DIR / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    data = yaml.safe_load(frontmatter)
    assert data["name"] == "citecraft-multi-agent"
    assert "1-minute demo path" in data["description"]

    openai_yaml = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    interface = openai_yaml["interface"]
    assert interface["display_name"] == "CiteCraft Multi-Agent"
    assert "$citecraft-multi-agent" in interface["default_prompt"]


def test_repo_scoped_agents_exist_with_required_fields():
    expected = [
        "citecraft-repo-explorer.toml",
        "citecraft-pipeline-developer.toml",
        "citecraft-demo-shell-designer.toml",
        "citecraft-growth-editor.toml",
        "citecraft-trace-reviewer.toml",
    ]
    for filename in expected:
        path = AGENT_DIR / filename
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert 'name = "' in text
        assert 'description = "' in text
        assert "developer_instructions = " in text
