## Cloud Run Python CRUD Example
## Simple Flask CRUD API suitable for packaging and deploying to Google Cloud Run.

## Quickstart:
## 1. Log into gcloud
## 2. Configure docker  (make sure to specify appropriate region)
## 3. Set email address as default account
```bash
gcloud auth login
gcloud auth configure-docker us-east4-docker.pkg.dev
gcloud config set account bipin.vidyarthi@gmail.com
```

## 4. Deploy to Cloud Run
```bash
docker build -t us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo/my-image:v1 .
docker push us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo/my-image:v1
```

# Local run

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
