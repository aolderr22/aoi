import json
import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

def load_data():
    load_dotenv()
    # Read configuration
    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    print(f"Loading data from Azure Blob Storage: {account_url}")
    container_name = os.environ["AZURE_STORAGE_CONTAINER"]
    blob_name = "characters/mock_characters.json"

    # Authenticate using your existing az login
    credential = DefaultAzureCredential()

    try:
        # Connect to Azure Blob Storage
        service = BlobServiceClient(
            account_url=account_url,
            credential=credential,
        )

        # Download the JSON file
        blob = service.get_blob_client(
            container=container_name,
            blob=blob_name,
        )

        json_bytes = blob.download_blob().readall()

        # Convert JSON into a Python object (usually a list or dict)
        data = json.loads(json_bytes.decode("utf-8"))

        return data

    finally:
        credential.close()