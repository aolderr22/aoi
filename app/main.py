from fastapi import FastAPI
from pydantic import BaseModel
from app.llm.response_generator import ResponseGenerator

app = FastAPI(
    title="AOI",
    description="AI assistant for recommending software engineering work items.",
    version="1.0.0",
)

generator = ResponseGenerator()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {
        "status": "running"
    }

@app.post("/ask")
def ask(request: QuestionRequest):

    response = generator.generate(
        request.question
    )

    return response