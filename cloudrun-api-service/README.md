# Cloud Run Python CRUD Example

Simple Flask CRUD API suitable for packaging and deploying to Google Cloud Run.

# Set email address as default account
gcloud config set account bipin.vidyarthi@gmail.com

Quickstart:

# Build the image in Google artifact registry path: "us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo"
docker build -t us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo/my-image:v1 .


# Push the completed layers to Google Artifact Registry
docker push us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo/my-image:v1

Local run

```bash
pip install -r requirements.txt
python main.py
# or with Docker
docker build -t cloudrun-api-service .
docker run -p 8080:8080 cloudrun-api-service
```

Notes
- This example uses SQLite for simplicity; Cloud Run containers are ephemeral. For production use, connect to Cloud SQL or another managed database.

API
- GET `/items` — list items
- GET `/items/<id>` — get item
- POST `/items` — create item JSON {"name": "...", "description": "..."}
- PUT `/items/<id>` — update
- DELETE `/items/<id>` — delete
