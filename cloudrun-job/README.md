# Cloud Run Job Example

This is a minimal dummy Cloud Run job that runs once, prints status messages, and exits cleanly.

## Build and run locally

```bash
docker build -t cloudrun-job .
docker run --rm cloudrun-job
```

## Customize runtime

The job supports the following optional arguments and environment variables:

- `--message` / `JOB_MESSAGE` — message to print
- `--iterations` / `JOB_ITERATIONS` — number of dummy work iterations
- `--delay` / `JOB_DELAY_SECONDS` — seconds to wait between iterations

Example:
```bash
docker run --rm cloudrun-job python main.py --message "Hello Job" --iterations 5 --delay 0.5
```

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
docker build -t us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo/my-job-image:v5 .
docker push us-east4-docker.pkg.dev/cloud-run-dev-504707/cloud-run-repo/my-job-image:v5
```