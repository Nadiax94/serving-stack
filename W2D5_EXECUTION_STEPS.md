# W2D5 Docker Compose - Execution Steps

## Project
Repository:
Nadiax94/serving-stack

## Objective

Move from manual docker run to Docker Compose deployment.

The service should run using:
- compose.yaml
- .env configuration
- model cache volume
- healthcheck
- API authentication


# 1. Environment Setup

Create .env file:

IMAGE=nadiax/aidc-serving:cpu-v4
MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
HOST_PORT=8000
API_KEY=mysecretkey123
MAX_TOKENS=64


# 2. Docker Compose Configuration

Create compose.yaml.

Services:
- serving

Configuration:
- Image from registry
- Port mapping
- Environment variables
- HuggingFace cache volume
- Restart policy
- Healthcheck


# 3. Start Service

Run:

docker compose up -d


Check status:

docker compose ps


Expected:

STATUS: healthy


# 4. Test Health Endpoint

Run:

curl http://localhost:8000/health


Expected:

HTTP 200


# 5. Test Model Endpoint

Without API Key:

curl http://localhost:8000/v1/models


Expected:

401 Unauthorized


With API Key:

curl \
-H "Authorization: Bearer mysecretkey123" \
http://localhost:8000/v1/models


Expected:

200 OK


# 6. Test Chat Completion

Run:

curl http://localhost:8000/v1/chat/completions \
-H "Authorization: Bearer mysecretkey123" \
-H "Content-Type: application/json" \
-d '{"model":"Qwen/Qwen2.5-0.5B-Instruct","messages":[{"role":"user","content":"Say hi"}],"max_tokens":8}'


Expected:

chat.completion response


# 7. Docker Image Versions

cpu-v1:
Original CPU image

cpu-v2:
Added environment configuration

cpu-v3:
Added API Key middleware

cpu-v4:
Final working version


# 8. Final Verification

Run:

docker compose ps

Verify:

- Container healthy
- API available
- Authentication working


# 9. GitHub Upload

Check changes:

git status


Add files:

git add .


Commit:

git commit -m "Complete W2D5 Docker Compose deployment and API authentication"


Push:

git push origin main


# Final Result

W2D5 Completed Successfully

PASS:
- Docker Compose
- Healthcheck
- Model Serving
- API Authentication
- GitHub Upload
