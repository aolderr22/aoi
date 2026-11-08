import os
from dotenv import load_dotenv
from azure.identity import (DefaultAzureCredential, get_bearer_token_provider)
from azure_loaders import (load_employee_data, load_task_data)
from agents import (get_skill_similarity_investigator_agent, get_skill_matching_agent)
from employee_services import rank_employee_task_matches
from language_models import (get_embeddings_model, get_primary_language_model)

def main():
    load_dotenv()

    azure_foundry_project_endpoint = os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT")
    azure_foundry_model_endpoint = os.getenv("AZURE_FOUNDRY_MODEL_ENDPOINT")
    azure_foundry_model_name = os.getenv("AZURE_FOUNDRY_MODEL_NAME")
    azure_foundry_embedding_model_name = os.getenv("AZURE_FOUNDRY_EMBEDDING_MODEL_NAME")
    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    container_name = os.environ["AZURE_STORAGE_CONTAINER_EMPLOYEES"]
    blob_name = os.environ["AZURE_STORAGE_BLOB_NAME_EMPLOYEES"]

    credential = DefaultAzureCredential()

    token_provider = get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    )
    employee_data = load_employee_data(account_url, container_name, blob_name)
    task_data = load_task_data(account_url, container_name, blob_name)

    primary_language_model = get_primary_language_model(azure_foundry_model_name, azure_foundry_project_endpoint, token_provider)
    embeddings_model = get_embeddings_model(azure_foundry_embedding_model_name, azure_foundry_model_endpoint, token_provider)
    skill_similarity_investigator_agent = get_skill_similarity_investigator_agent(primary_language_model)
    skill_matching_agent = get_skill_matching_agent(primary_language_model)

    print("task_data:", task_data)
    print("employee_data:", employee_data)

    learning_ranked, leadership_ranked = rank_employee_task_matches(task_data, employee_data, skill_similarity_investigator_agent, skill_matching_agent)

    print("Learning ranked:", learning_ranked)
    print("Leadership ranked:", leadership_ranked)

    return 0

if __name__ == "__main__":
    exit(main())