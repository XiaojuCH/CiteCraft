---
name: citecraft-multi-agent
description: Coordinate repo-scoped subagents to improve the CiteCraft repository. Use when work spans multiple surfaces such as `src/workbench`, `apps/web`, `examples`, `docs/assets`, or `README.md`; when you need a main-agent plan plus explorer, implementer, and reviewer handoffs; or when you want to evolve the repo without breaking the 1-minute demo path.
---

# CiteCraft Multi-Agent

## Overview

Use this skill when a CiteCraft task is large enough that one agent should not both explore and implement everything.
The default pattern is: `main agent scopes -> read-only exploration -> one primary writer lane -> review -> verification`.

## Quick Start

Use the repo-local subagents in `.codex/agents/`:

- `citecraft-repo-explorer`
- `citecraft-pipeline-developer`
- `citecraft-demo-shell-designer`
- `citecraft-growth-editor`
- `citecraft-trace-reviewer`

Read [references/repo-map.md](references/repo-map.md) first when the task touches unfamiliar repo surfaces.
Read [references/workflow-patterns.md](references/workflow-patterns.md) when you need prompt patterns or coordination rules.

## Workflow

### 1. Freeze the target

- State the exact outcome first: repo capability, demo surface, growth surface, or traceability fix.
- Name the primary surfaces before spawning helpers.
- Default to one writer lane unless file sets are clearly disjoint.

### 2. Explore before writing

- Spawn `citecraft-repo-explorer` when the task crosses subsystem boundaries or the touched files are not obvious.
- If the task is already localized, keep exploration light and move faster.
- Require the explorer to return touched paths, current behavior, risks, and validation points.

### 3. Choose the writer lane

- Use `citecraft-pipeline-developer` for core Python changes.
- Use `citecraft-demo-shell-designer` for demo shell, poster, screenshot, or share surface work.
- Use `citecraft-growth-editor` for README and contributor-facing docs.
- Only use more than one writer if the file boundaries are clean.

### 4. Review before merging

- Run `citecraft-trace-reviewer` on any change that touches:
  - traces
  - deliverables
  - poster or homepage claims
  - sample projects
  - expected outputs
- Findings should be organized by severity with file references.

### 5. Verify the golden path

- Re-run focused tests for touched surfaces.
- If sample outputs or screenshots are affected, regenerate them intentionally.
- Keep the `1-minute demo` stable unless the task explicitly changes the demo story.

## Routing Guide

- `contracts / pipeline / providers / renderers` -> `citecraft-pipeline-developer`
- `homepage / poster / sources view / screenshots` -> `citecraft-demo-shell-designer`
- `README / docs / contributor onboarding / positioning copy` -> `citecraft-growth-editor`
- `cross-cutting repo map or risk scan` -> `citecraft-repo-explorer`
- `final quality gate` -> `citecraft-trace-reviewer`

## Guardrails

- Do not let multiple writer agents modify the same file set concurrently.
- Do not let a reviewer silently become a writer.
- Do not optimize for agent complexity over visible repo progress.
- Do not claim README capabilities that the actual demo cannot produce.
- Prefer real artifacts over conceptual promises.

## Example Prompt Starters

- `Use $citecraft-multi-agent to improve the trace inspection flow without breaking the current poster route.`
- `Use $citecraft-multi-agent to add a new deliverable type with contract, renderer, sample, and review coverage.`
- `Use $citecraft-multi-agent to refresh the growth surfaces after a demo-shell change, while keeping claims honest.`

## Resources

- Repo topology and when to route work to which subsystem: [references/repo-map.md](references/repo-map.md)
- Prompt patterns and sequencing rules derived from the multi-agent training notes: [references/workflow-patterns.md](references/workflow-patterns.md)
