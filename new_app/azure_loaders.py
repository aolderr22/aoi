import os
import json
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

def load_employee_data(account_url, container_name, blob_name):
    """Download employee JSON data from Azure Blob Storage."""

    credential = DefaultAzureCredential()

    try:
        service = BlobServiceClient(
            account_url=account_url,
            credential=credential,
        )

        blob = service.get_blob_client(
            container=container_name,
            blob=blob_name,
        )

        json_bytes = blob.download_blob().readall()
        data = json.loads(json_bytes.decode("utf-8"))

        # Accept either a list or {"employees": [...]}.
        if isinstance(data, dict):
            data = data.get("employees")

        if not isinstance(data, list):
            raise ValueError(
                "Employee data must be a JSON list or an "
                "object containing an 'employees' list."
            )

        return data

    finally:
        credential.close()

def load_task_data(account_url, container_name, blob_name):
    """Download task JSON data from Azure Blob Storage."""
    
    credential = DefaultAzureCredential()

    try:
        service = BlobServiceClient(
            account_url=account_url,
            credential=credential,
        )

        blob = service.get_blob_client(
            container=container_name,
            blob=blob_name,
        )

        json_bytes = blob.download_blob().readall()
        data = json.loads(json_bytes.decode("utf-8"))

        # Accept either a list or {"tasks": [...]}.
        if isinstance(data, dict):
            data = data.get("tasks")

        if not isinstance(data, list):
            raise ValueError(
                "Task data must be a JSON list or an "
                "object containing a 'tasks' list."
            )

        return data

    finally:
        credential.close()