# W2D2 - Model Serving API

This project wraps `Qwen/Qwen2.5-0.5B-Instruct` behind an OpenAI-compatible FastAPI service running on CPU.

## Implemented Endpoints

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

Streaming is optional for this lab and is not implemented.

## Run the Server

```bash
cd app
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Verify

From the project folder:

```bash
python verify.py
```

### Verification Result

```text
model: Qwen/Qwen2.5-0.5B-Instruct
completion content: 'Hello.'
usage: {'prompt_tokens': 35, 'completion_tokens': 3, 'total_tokens': 38}
streaming: not implemented (optional this week)
GREEN CHECK: PASS
```

## Model

`Qwen/Qwen2.5-0.5B-Instruct`

## Notes

Model generation runs synchronously on CPU and blocks while generating. Concurrency is intentionally not handled in this week-2 implementation.
