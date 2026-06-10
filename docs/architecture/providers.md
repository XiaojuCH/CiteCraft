# Provider Architecture

The provider layer is intentionally narrow in P0.

It does not own ingestion, evidence selection, trace binding, rendering, or orchestration.
It only rewrites one already-selected deliverable node at a time.

## Providers

- `deterministic`: default provider that returns seed text unchanged.
- `openai-compatible`: optional chat-completions provider for OpenAI-compatible APIs.

## Configuration

```powershell
$env:WORKBENCH_PROVIDER="openai-compatible"
$env:WORKBENCH_API_KEY="..."
$env:WORKBENCH_MODEL="gpt-4.1-mini"
$env:WORKBENCH_BASE_URL="https://api.openai.com/v1"
D:\anaconda3\python.exe -m workbench.pipeline.run examples/academia/demo-01 --provider openai-compatible
```

If `WORKBENCH_API_KEY` is missing, or if the request fails, the provider falls
back to deterministic seed text by default. This keeps the 1-minute demo stable.

Set `WORKBENCH_FALLBACK_ON_ERROR=0` to fail loudly during provider development.

## Product Rule

Providers should improve wording and structure, not invent facts.
Evidence selection and citation binding remain in the workbench core.
