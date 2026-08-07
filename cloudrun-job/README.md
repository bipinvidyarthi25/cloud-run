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

## Deploy to Cloud Run

Use `gcloud run jobs create` to deploy this container image as a Cloud Run job.
