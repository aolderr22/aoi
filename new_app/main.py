import os
from dotenv import load_dotenv
from azure.identity import (DefaultAzureCredential, get_bearer_token_provider)
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .agents import (get_skill_similarity_investigator_agent, get_skill_matching_agent)
from .azure_loaders import (load_employee_data, load_task_data)
from .employee_services import rank_employee_task_matches
from .language_models import (get_embeddings_model, get_primary_language_model)
from .schemas import (Employee, Task)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    azure_foundry_project_endpoint = os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT")
    azure_foundry_model_endpoint = os.getenv("AZURE_FOUNDRY_MODEL_ENDPOINT")
    azure_foundry_model_name = os.getenv("AZURE_FOUNDRY_MODEL_NAME")
    azure_foundry_embedding_model_name = os.getenv("AZURE_FOUNDRY_EMBEDDING_MODEL_NAME")
    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    container_name_employees = os.environ["AZURE_STORAGE_CONTAINER_EMPLOYEES"]
    blob_name_employees = os.environ["AZURE_STORAGE_BLOB_NAME_EMPLOYEES"]
    container_name_tasks = os.environ["AZURE_STORAGE_CONTAINER_TASKS"]
    blob_name_tasks = os.environ["AZURE_STORAGE_BLOB_NAME_TASKS"]

    credential = DefaultAzureCredential()

    token_provider = get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    )
    app.state.employee_data = load_employee_data(account_url, container_name_employees, blob_name_employees)
    app.state.task_data = load_task_data(account_url, container_name_tasks, blob_name_tasks)

    primary_language_model = get_primary_language_model(azure_foundry_model_name, azure_foundry_project_endpoint, token_provider)
    app.state.primary_language_model = primary_language_model

    embeddings_model = get_embeddings_model(azure_foundry_embedding_model_name, azure_foundry_model_endpoint, token_provider)
    app.state.embeddings_model = embeddings_model

    app.state.skill_similarity_investigator_agent = get_skill_similarity_investigator_agent(primary_language_model)
    app.state.skill_matching_agent = get_skill_matching_agent(primary_language_model)

    yield

    # Shutdown operations
    credential.close()

    print("AOI Employee API shut down.")

app = FastAPI(
    title="AOI Employee API",
    description="Employee data API backed by Azure Blob Storage.",
    version="0.2.0",
    lifespan=lifespan,
)

@app.get(
    "/employees",
    name="list_employees",
    response_model=list[Employee],
)
def list_employees():
    """Return all employee records."""
    return app.state.employee_data

@app.get(
    "/createPods",
    name="create_pods",
)
def create_pods():
    learning_ranked, leadership_ranked = rank_employee_task_matches(app.state.task_data,
                                                                    app.state.employee_data, 
                                                                    app.state.skill_similarity_investigator_agent, 
                                                                    app.state.skill_matching_agent)
    return (learning_ranked, leadership_ranked)