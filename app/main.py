import logging
import os
from contextlib import asynccontextmanager

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.ai_service import answer_question
from app.azure_data import load_data
from app.schemas import AskRequest, AskResponse, HealthResponse

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Azure clients and load data at application startup."""
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_name = (
        os.getenv("MODEL_NAME")
        or os.getenv("MODEL_DEPLOYMENT_NAME")
    )

    if not project_endpoint:
        raise RuntimeError("PROJECT_ENDPOINT is missing from .env")

    if not model_name:
        raise RuntimeError(
            "Set MODEL_NAME or MODEL_DEPLOYMENT_NAME in .env"
        )

    credential = DefaultAzureCredential()
    project_client = None

    try:
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        )

        app.state.openai_client = project_client.get_openai_client()
        app.state.model_name = model_name
        app.state.characters = load_data()

        logger.info("Azure clients initialized and JSON data loaded.")
        yield

    finally:
        if project_client is not None:
            project_client.close()

        credential.close()

app = FastAPI(
    title="AOI Question Answering API",
    description="Answers questions using JSON data in Azure Blob Storage.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/health", response_model=HealthResponse)
def health_check():
    data = app.state.characters

    if isinstance(data, (list, dict)):
        record_count = len(data)
    else:
        record_count = 1

    return {
        "status": "ok",
        "data_records": record_count,
    }

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        answer = answer_question(
            openai_client=app.state.openai_client,
            model_name=app.state.model_name,
            characters=app.state.characters,
            question=request.question,
        )

        return AskResponse(
            question=request.question,
            answer=answer,
        )

    except Exception as exc:
        logger.exception("Failed to generate an answer.")
        raise HTTPException(
            status_code=502,
            detail="The AI service failed to generate an answer.",
        ) from exc