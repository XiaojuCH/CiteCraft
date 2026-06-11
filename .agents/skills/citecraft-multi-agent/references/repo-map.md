# Repo Map

Use this file when the task touches more than one surface.

## Core Product Surfaces

- `src/workbench/contracts`
  Shared structured models and project config. Touch here when interfaces or canonical shapes change.
- `src/workbench/sources`
  Input adapters for PDF, URL, and folder ingestion.
- `src/workbench/evidence`
  Evidence selection, indexing, and trace attachment helpers.
- `src/workbench/deliverables`
  Deliverable generators for `brief`, `literature_matrix`, and `slides`.
- `src/workbench/providers`
  Deterministic and model-backed wording layer. Keep this narrow.
- `src/workbench/renderers`
  Markdown and HTML rendering for deliverables.
- `src/workbench/pipeline`
  End-to-end orchestration for the deterministic golden path.

## Demo And Growth Surfaces

- `apps/web`
  Local demo shell, sources browser, trace inspector, homepage, poster route.
- `examples/academia/demo-01`
  Golden path sample for the academia wedge.
- `examples/research/demo-01`
  Second wedge proving category breadth beyond academia.
- `docs/assets`
  Real screenshot assets used by README and sharing surfaces.
- `README.md`
  Primary growth surface. Keep claims aligned with reality.

## High-Risk Change Types

- Contract changes that do not update renderers or examples
- Trace changes that weaken source chunk visibility
- Poster or README changes that overstate current product capability
- Provider changes that break deterministic fallback

## Default Validation By Surface

- `src/workbench/**`
  Run the Python test suite.
- `apps/web/**`
  Run the Python test suite and, when visuals change materially, regenerate poster or README screenshots.
- `examples/**`
  Regenerate expected outputs for the touched sample project when behavior changes intentionally.
- `README.md` or `docs/assets/**`
  Check screenshots still match the live demo shell.

