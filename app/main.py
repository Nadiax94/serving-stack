"""serving-stack: the FastAPI service (week 2, CPU, tiny model).

Completed solution for the required week-2 routes:
- GET /health
- GET /v1/models
- POST /v1/chat/completions (non-streaming)

Run:
    uvicorn main:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import os
import time
import uuid

import torch
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer

from schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Choice,
    HealthResponse,
    ModelCard,
    ModelList,
    ResponseMessage,
    Usage,
)

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-0.5B-Instruct")

app = FastAPI(title="serving-stack", version="wk2")

# Load once at import time. CPU only this week.
print(f"loading {MODEL_ID} on cpu ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
)
model.to("cpu")
model.eval()
print("model ready")


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness/readiness endpoint."""
    return HealthResponse(status="ok", model=MODEL_ID)


# ---------------------------------------------------------------------------
# GET /v1/models
# ---------------------------------------------------------------------------
@app.get("/v1/models", response_model=ModelList)
def list_models() -> ModelList:
    """Return the single model served by this week-2 service."""
    return ModelList(
        data=[
            ModelCard(
                id=MODEL_ID,
                created=int(time.time()),
            )
        ]
    )


# ---------------------------------------------------------------------------
# POST /v1/chat/completions -- required non-streaming implementation
# ---------------------------------------------------------------------------
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
def chat_completions(req: ChatCompletionRequest) -> ChatCompletionResponse:
    """Generate one OpenAI-compatible non-streaming chat completion."""

    # Build the Qwen chat prompt and tokenize it.
    input_ids = tokenizer.apply_chat_template(
        [message.model_dump() for message in req.messages],
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )

    prompt_tokens = input_ids.shape[1]

    generation_kwargs = {
        "max_new_tokens": req.max_tokens,
        "do_sample": req.temperature > 0,
    }
    if req.temperature > 0:
        generation_kwargs["temperature"] = req.temperature

    # Generation is intentionally synchronous/blocking this week.
    with torch.no_grad():
        output = model.generate(
            input_ids,
            **generation_kwargs,
        )

    # Decode only newly generated tokens, not the prompt.
    new_tokens = output[0][prompt_tokens:]
    completion_tokens = len(new_tokens)

    text = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True,
    ).strip()

    finish_reason = (
        "length"
        if completion_tokens >= req.max_tokens
        else "stop"
    )

    return ChatCompletionResponse(
        id="chatcmpl-" + uuid.uuid4().hex,
        created=int(time.time()),
        model=req.model,
        choices=[
            Choice(
                message=ResponseMessage(
                    content=text,
                ),
                finish_reason=finish_reason,
            )
        ],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


# Streaming is optional for the green check and is intentionally not included.
