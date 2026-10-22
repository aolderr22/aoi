import json
import os

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

def load_data():
    """Download and parse the JSON data from Azure Blob Storage."""
    load_dotenv()

    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    container_name = os.environ["AZURE_STORAGE_CONTAINER"]
    blob_name = os.getenv("AZURE_STORAGE_BLOB_NAME")

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
        return json.loads(json_bytes.decode("utf-8"))

    finally:
        credential.close()