#!/usr/bin/env bash

set -e

echo "=== W2D5 Compose Verification ==="

# Check files
echo "[1/6] Checking required files..."

test -f .env || { echo "FAIL: .env missing"; exit 1; }
test -f compose.yaml || { echo "FAIL: compose.yaml missing"; exit 1; }

echo "PASS: Required files exist"


# Check docker compose
echo "[2/6] Checking Docker Compose..."

docker compose ps >/dev/null 2>&1 || {
    echo "FAIL: docker compose unavailable"
    exit 1
}

echo "PASS: Docker Compose available"


# Check container health
echo "[3/6] Checking container health..."

STATUS=$(docker compose ps --format json | grep -o "healthy" || true)

if [ "$STATUS" != "healthy" ]; then
    echo "FAIL: Container is not healthy"
    docker compose ps
    exit 1
fi

echo "PASS: Container healthy"


# Check health endpoint
echo "[4/6] Checking /health..."

HEALTH=$(curl -s http://localhost:8000/health)

echo "$HEALTH" | grep -q "ok" || {
    echo "FAIL: /health failed"
    exit 1
}

echo "PASS: /health"


# Check API key protection
echo "[5/6] Checking API Key protection..."

NO_KEY=$(curl -s -o /dev/null -w "%{http_code}" \
http://localhost:8000/v1/models)

if [ "$NO_KEY" != "401" ]; then
    echo "FAIL: /v1/models without key returned $NO_KEY"
    exit 1
fi

WITH_KEY=$(curl -s -o /dev/null -w "%{http_code}" \
-H "Authorization: Bearer mysecretkey123" \
http://localhost:8000/v1/models)

if [ "$WITH_KEY" != "200" ]; then
    echo "FAIL: /v1/models with key returned $WITH_KEY"
    exit 1
fi

echo "PASS: API Key protection"


# Final
echo "[6/6] Checking chat endpoint..."

CHAT=$(curl -s \
-H "Authorization: Bearer mysecretkey123" \
-H "Content-Type: application/json" \
-d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Say hi"}],"max_tokens":8}' \
http://localhost:8000/v1/chat/completions)

echo "$CHAT" | grep -q "chat.completion" || {
    echo "FAIL: chat completion failed"
    exit 1
}

echo "PASS: Chat completion"

echo ""
echo "GREEN CHECK: PASS"
