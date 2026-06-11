# Workflow Patterns

These patterns adapt the multi-agent training notes to the CiteCraft repo.

## Pattern 1: Cross-Cutting Improvement

Use when a task spans contracts, pipeline, and shell.

1. Main agent states the outcome and touched surfaces.
2. `citecraft-repo-explorer` maps current behavior and risks.
3. Main agent freezes implementation scope.
4. One writer agent implements the primary change.
5. `citecraft-trace-reviewer` checks regressions and missing tests.
6. Main agent verifies outputs and summarizes.

Use this for:

- adding a deliverable type
- changing trace behavior
- changing provider output rules

## Pattern 2: Demo Surface Upgrade

Use when the task is mostly in `apps/web`, `docs/assets`, or `README.md`.

1. `citecraft-repo-explorer` or the main agent identifies current UI surfaces.
2. `citecraft-demo-shell-designer` implements the route, page, poster, or screenshot flow.
3. `citecraft-growth-editor` updates README or share copy if needed.
4. `citecraft-trace-reviewer` checks that visual claims still match the product.

Use this for:

- homepage redesigns
- poster route updates
- screenshot refreshes

## Pattern 3: Growth Copy Refresh

Use when the product changed and repo-facing copy is now stale.

1. Main agent identifies the product change that should change the story.
2. `citecraft-growth-editor` updates README and docs.
3. `citecraft-trace-reviewer` checks honesty and repo reality.

Use this for:

- README positioning shifts
- onboarding docs
- contributor workflow docs

## Prompt Template For The Main Agent

```text
Use $citecraft-multi-agent for this repo task.

Outcome:
[one clear sentence]

Touched surfaces:
- [path or subsystem]
- [path or subsystem]

Constraints:
- keep the 1-minute demo stable
- do not let multiple writers touch the same file set
- regenerate real assets only if the visible surface changes
```

## Prompt Template For The Explorer

```text
Use $citecraft-repo-explorer on this repo task.

Stay read-only.
Inspect:
- [paths]

Return:
1. touched files
2. current behavior
3. risks
4. validation checklist
```

## Prompt Template For The Reviewer

```text
Use $citecraft-trace-reviewer on this repo task.

Stay review-only.
Prioritize:
- traceability regressions
- demo path regressions
- missing tests
- README or poster overclaiming
```

