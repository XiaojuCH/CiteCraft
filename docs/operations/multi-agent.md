# Multi-Agent Repo Workflow

This repo includes project-scoped subagents and a project-scoped skill so contributors can reuse the same collaboration pattern we use internally.

## Project-Scoped Skill

- `.agents/skills/citecraft-multi-agent/`

Use it when a task spans multiple repo surfaces, or when you want to split work into exploration, implementation, and review without losing the golden demo path.

## Project-Scoped Subagents

- `.codex/agents/citecraft-repo-explorer.toml`
- `.codex/agents/citecraft-pipeline-developer.toml`
- `.codex/agents/citecraft-demo-shell-designer.toml`
- `.codex/agents/citecraft-growth-editor.toml`
- `.codex/agents/citecraft-trace-reviewer.toml`

## Default Repo Pattern

1. Use the main agent to freeze the outcome and touched surfaces.
2. Use the explorer first when boundaries are unclear.
3. Use exactly one writer lane unless file sets are clearly disjoint.
4. Use the reviewer before calling the work done.
5. Re-run tests and regenerate assets only when the touched surface requires it.

## Why This Exists

- Keeps the `1-minute demo` stable while the repo evolves
- Prevents multiple writer agents from colliding on the same files
- Keeps README and poster claims aligned with actual product behavior
- Makes contribution patterns easier to onboard and scale

