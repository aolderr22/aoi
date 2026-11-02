import os
from dotenv import load_dotenv
from azure.identity import (DefaultAzureCredential, get_bearer_token_provider)

def main():
    load_dotenv()

    azure_project_endpoint = os.getenv("AZURE_PROJECT_ENDPOINT")
    azure_model_endpoint = os.getenv("AZURE_MODEL_ENDPOINT")
    azure_model_name = os.getenv("AZURE_MODEL_NAME")
    azure_embedding_model_name = os.getenv("AZURE_EMBEDDING_MODEL_NAME")
    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    container_name = os.environ["AZURE_STORAGE_CONTAINER_EMPLOYEES"]
    blob_name = os.environ["AZURE_STORAGE_BLOB_NAME_EMPLOYEES"]

    credential = DefaultAzureCredential()

    token_provider = get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    )
    print('Token provider initialized successfully.')

    return 0