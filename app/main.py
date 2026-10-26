import logging
import os
from contextlib import asynccontextmanager
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from app.azure_data import (load_employee_data, load_task_data)
from app.schemas import (
    Employee,
    HealthResponse,
    RecommendEmployeeRequest,
    EmployeeRecommendationResponse,
    Task,
)
from app.recommendation_service import (recommend_employee, map_employees_to_tasks)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Azure clients and load employee records."""
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_name = os.getenv("MODEL_NAME")

    if not project_endpoint:
        raise RuntimeError("PROJECT_ENDPOINT is missing from .env")

    if not model_name:
        raise RuntimeError("MODEL_NAME is missing from .env")

    credential = DefaultAzureCredential()
    project_client = None

    try:
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        )

        app.state.openai_client = project_client.get_openai_client()
        app.state.model_name = model_name
        app.state.employees = [
            Employee.model_validate(record)
            for record in load_employee_data()
        ]

        app.state.tasks = [
            Task.model_validate(record)
            for record in load_task_data()
        ]

        logger.info(
            "Azure clients initialized; loaded %s employees and %s tasks.",
            len(app.state.employees),
            len(app.state.tasks),
        )

        yield

    finally:
        if project_client is not None:
            project_client.close()
        credential.close()

app = FastAPI(
    title="AOI Employee API",
    description="Employee data API backed by Azure Blob Storage.",
    version="0.2.0",
    lifespan=lifespan,
)

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        data_records=len(app.state.employees),
        task_records=len(app.state.tasks),
    )

@app.get(
    "/employees",
    name="list_employees",
    response_model=list[Employee],
)
def list_employees():
    """Return all employee records."""
    return app.state.employees

@app.get(
    "/tasks",
    name="list_tasks",
    response_model=list[Task],
)
def list_tasks():
    """Return all task records."""
    return app.state.tasks

@app.post(
    "/recommend-employee",
    response_model=EmployeeRecommendationResponse,
)
def recommend_employee_endpoint(request: RecommendEmployeeRequest):
    try:
        result = recommend_employee(
            openai_client=app.state.openai_client,
            model_name=app.state.model_name,
            employees=app.state.employees,
            task=request.task,
        )

        return result

    except Exception as exc:
        logger.exception("Employee recommendation failed.")
        raise HTTPException(
            status_code=502,
            detail="Could not generate an employee recommendation.",
        ) from exc

@app.post(
    "/map-employees-to-tasks",
    response_model=str,
)
def map_employees_to_tasks_endpoint():
    result = map_employees_to_tasks(
        openai_client=app.state.openai_client,
        model_name=app.state.model_name,
        employees=app.state.employees,
        tasks=app.state.tasks,
    )

    return result