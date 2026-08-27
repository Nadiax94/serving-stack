W2D5 Docker Compose Deployment – Evidence Steps


Step 1 — Build Final Docker Image (CPU-v4)

<img width="1148" height="470" alt="image" src="https://github.com/user-attachments/assets/3e50fdf2-83e4-4748-9de3-fccb1aada823" />

Command executed:

docker build -t nadiax/aidc-serving:cpu-v4 .

Evidence:

Docker image built successfully.
Final image created:
nadiax/aidc-serving:cpu-v4


Step 2 — Verify Docker Image Availability

<img width="892" height="47" alt="image" src="https://github.com/user-attachments/assets/942c0aca-39bb-496b-ae76-440d3a938534" />

docker images | grep cpu-v4

Evidence Result:

nadiax/aidc-serving:cpu-v4

Image size:

1.61GB



Step 3 — Deploy Application Using Docker Compose


Description:
Stopped the previous container and started the service using Docker Compose.

Commands executed:

docker compose down

Then:

docker compose up -d

Evidence:

Network created successfully.
Container started successfully.

Container:

serving-stack-serving-1

Step 4 — Verify Container Health Status

Description:
Checked that the service is running correctly and passed the health check.

Command executed:

docker compose ps

Expected Result:

STATUS: Up (healthy)

Evidence:

IMAGE: nadiax/aidc-serving:cpu-v4
STATUS: healthy
PORT: 8000

Step 5 — Test API Authentication Without API Key

Description:
Verified that /v1/models endpoint rejects unauthorized requests.

Command executed:

curl -s -o /dev/null -w "%{http_code}\n" \
http://localhost:8000/v1/models

Expected Result:

401

Evidence:

Unauthorized request correctly blocked.

Step 6 — Test API Authentication With API Key

Description:
Verified that authorized requests are accepted.

Command executed:

curl -s -o /dev/null -w "%{http_code}\n" \
-H "Authorization: Bearer mysecretkey123" \
http://localhost:8000/v1/models

Expected Result:

200

Evidence:

Authorized request successfully returned:

200 OK


Step 7 — Verify Health Endpoint

Description:
Confirmed that the health endpoint remains publicly accessible.

Command executed:

curl -s -o /dev/null -w "%{http_code}\n" \
http://localhost:8000/health

Expected Result:

200

Evidence:

Health endpoint returned successfully.

<img width="1170" height="408" alt="image" src="https://github.com/user-attachments/assets/721c9ba2-a493-4e7c-b951-8d37dfc67b7a" />


Step 8 — Run Automated Verification Script

Description:
Executed the custom W2D5 verification script.

Command executed:

./verify_w2d5.sh

Verification checks:

Required files exist
Docker Compose available
Container health
API availability

Evidence:

Verification started successfully.


<img width="590" height="308" alt="image" src="https://github.com/user-attachments/assets/32294763-d686-4fb5-bee6-e595fe6520c6" />



Final Status

✅ Docker Compose Deployment Completed
✅ CPU-v4 Image Built
✅ Container Healthy
✅ API Key Authentication Enabled
✅ Health Endpoint Working
✅ GitHub Repository Updated
