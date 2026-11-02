import os
from dotenv import load_dotenv
from pathlib import Path
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

load_dotenv()

credential = DefaultAzureCredential()

service = BlobServiceClient(
    account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
    credential=credential,
)

container_name = os.environ["AZURE_STORAGE_CONTAINER_TASKS"]

container = None
try:
    container = service.create_container(name=container_name)
    print(f"Created container: {container_name}")
except ResourceExistsError:
    container = service.get_container_client(container_name)
    print(f"Container already exists: {container_name}")

# Path to your separate JSON file
json_path = Path("data/tasks.json")

# Choose the destination name in Azure Blob Storage
blob_name = "tasks/tasks.json"

# Upload the file
blob = container.get_blob_client(blob_name)

with json_path.open("rb") as file:
    blob.upload_blob(file, overwrite=True)

print(f"Successfully uploaded {json_path.name}")
print(f"Azure blob name: {blob_name}")