"""serving-stack: the FastAPI service."""

from __future__ import annotations

import os
import time
import uuid

import torch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
API_KEY = os.environ.get("API_KEY", "")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "64"))


app = FastAPI(title="serving-stack", version="wk2")


# API Key protection for /v1/*
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path.startswith("/v1/"):
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {API_KEY}":
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"},
            )

    return await call_next(request)


# Load model
print(f"loading {MODEL_ID} on cpu ...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
)

model.to("cpu")
model.eval()

print("model ready")


# -------------------------
# GET /health
# -------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_ID,
    }


# -------------------------
# GET /v1/models
# -------------------------
@app.get("/v1/models")
def models():
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_ID,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "aidc",
            }
        ],
    }


# -------------------------
# POST /v1/chat/completions
# -------------------------
@app.post("/v1/chat/completions")
def chat_completion(request: ChatCompletionRequest):

    prompt = request.messages[-1].content

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    inputs = {k: v.to("cpu") for k, v in inputs.items()}

    max_tokens = min(
        request.max_tokens or MAX_TOKENS,
        MAX_TOKENS,
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
        )

    generated = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    answer = generated[len(prompt):].strip()

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": MODEL_ID,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(inputs["input_ids"][0]),
            "completion_tokens": len(outputs[0]),
            "total_tokens": len(outputs[0]),
        },
    }
