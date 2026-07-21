# Model Validataion Tests

## Chat API (classic) and Responses API (newer)

Validate which Nebius Token Factory models
support the OpenAI-style **Chat Completions** API and the newer **Responses** API.

### Files

- [test_chat_and_responses_api.py](test_chat_and_responses_api.py) — single-model smoke test for both APIs
- [test_apis_for_all_models.py](test_apis_for_all_models.py) — bulk, parallel check across all models

### Running

1. **Set your API key**. Copy the sample env file and fill in your key:

```bash
cp env_sample.txt .env
# then edit .env and set NEBIUS_API_KEY=your_api_key_here
```

This is a [uv](https://docs.astral.sh/uv/) project.

```bash
uv sync
```

**`test_chat_and_responses_api.py`**

A minimal example that calls a single model using **both** the
Chat Completions API and the Responses API and prints the results.

```bash
uv run python test_chat_and_responses_api.py
```

**`test_apis_for_all_models.py`**

Lists every non-embedding model available in your Token Factory project and
checks (in parallel) which ones support each API. Prints a markdown table
summary when done.

```bash
uv run python test_apis_for_all_models.py
```
