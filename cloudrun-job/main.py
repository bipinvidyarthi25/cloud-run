import argparse
from datetime import datetime, timezone
import os
import io
import sys
import time
import json
import pandas as pd
import requests
from google.cloud import storage
from google.cloud import bigquery

# Setting up the timestamp for file naming and logging
current_timestamp = datetime.now(timezone.utc)
formatted_datetime = current_timestamp.strftime("%Y-%m-%d-%H%M%S")
API_URL = "https://fake-json-api.mock.beeceptor.com/companies"
BUCKET_NAME = "cloud-run-bkv"
DESTINATION_BLOB_NAME = f"api_data_{formatted_datetime}.csv"        
GCS_URI = f"gs://{BUCKET_NAME}/{DESTINATION_BLOB_NAME}"

project_id = "cloud-run-dev-504707"  # Replace with your GCP project ID
dataset_id = "ds_bipin_vidyarthi"  # Replace with your dataset ID
table_id = "company_master"      # Replace with your table ID
table_ref = f"{project_id}.{dataset_id}.{table_id}"

def save_api_data_to_bigquery(data: list) -> None:
    try:        
        # Data must be a list of dictionaries (rows), even for a single row
        rows_to_insert = []
        for row in data or []:  # Ensure data is iterable
            rows_to_insert.append({
                "id": int(row.get("id")) if row.get("id") is not None else None,
                "name": row.get("name"),
                "address": row.get("address"),
                "zip": row.get("zip"),
                "country": row.get("country"),
                "employeeCount": int(row.get("employeeCount")) if row.get("employeeCount") is not None else None,
                "industry": row.get("industry"),
                "marketCap": float(row.get("marketCap")) if row.get("marketCap") is not None else None,
                "domain": row.get("domain"),
                "logo": row.get("logo"),
                "ceoName": row.get("ceoName"),
                #"ingestion_date": current_timestamp.isoformat()  # Add ingestion timestamp
            })

        # Stream data into BigQuery
        bq_client = bigquery.Client()
        errors = bq_client.insert_rows_json(table_ref, rows_to_insert)

        # Check for API-level payload validation errors
        if errors == []:
            print("New rows have been successfully added.")
        else:
            print(f"Encountered errors while inserting rows: {errors}")
            raise
    except Exception as e:
        raise

def run_job() -> None:
    try:        
        # 1. Fetch data from the API
        print(f"Fetching companies data at {formatted_datetime}")

        data = requests.get(API_URL).json()

        print(f"Fetched {len(data)} companies.")
        
        # 2. Convert JSON data to a Pandas DataFrame & export to CSV string
        # 3. Adjust `data['items']` depending on where the array of records is located in your JSON response
        df = pd.DataFrame(data)
        csv_string = df.to_csv(index=False)
        
        # 4. Upload the CSV string directly to GCS bucket in-memory
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(DESTINATION_BLOB_NAME)
        print(f"Uploading CSV to GCS bucket '{BUCKET_NAME}' as '{DESTINATION_BLOB_NAME}'.")
        blob.upload_from_string(csv_string, content_type="text/csv")
        print(f"Finished uploading CSV to GCS bucket '{BUCKET_NAME}' as '{DESTINATION_BLOB_NAME}'.")

        # 5. Load the data into BigQuery
        save_api_data_to_bigquery(data)

        """
        # 3. Load the CSV data from GCS into BigQuery
        print(f"Loading CSV data from GCS into BigQuery.")
        bq_client = bigquery.Client()

        # 4. Configure the load job
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,      # Skip header row for CSV
            autodetect=True,          # Automatically infer schema columns/types
            jagged_rows=True,         # Allow rows with missing values
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND # Append data
        )
        
        # 5. Trigger the asynchronous load job
        print(f"Starting load job for {GCS_URI} into BigQuery table {dataset_id}.{table_id}.")
        load_job = bq_client.load_table_from_uri(
            GCS_URI,
            table_ref,
            job_config=job_config
        )
    
        # 6. Wait for the job to complete (blocks until finished)
        load_job.result()
        print(f"Finished loading CSV data from GCS into BigQuery.")
        """
    except Exception as e:
        raise


if __name__ == "__main__":
    try:
        run_job()
    except Exception as e:
        print(f"Job failed with error: {e}")
        sys.exit(1)  # Exit with code 1 to indicate failure to Cloud Run
    finally:
        print("Job completed.")
        sys.exit(0)  # Exit with code 0 to indicate success to Cloud Run
