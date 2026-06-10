# Deliverable Contracts

All P0 deliverables are structured models first.

- `brief`
- `literature_matrix`
- `slides`

Shared contract rules:

- every deliverable has `deliverable_id`, `deliverable_type`, `project_id`, `title`, `source_ids`, and `render_hints`
- every user-visible node has a deterministic `node_id`
- traceable nodes attach one or more `TraceAttachment` objects
- human-readable output is markdown-first, but markdown is not the only source of truth

