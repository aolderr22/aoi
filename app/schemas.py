from pydantic import BaseModel, Field

class Employee(BaseModel):
    id: int
    name: str
    position: str
    skill_map: dict[str, str]

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

class AskResponse(BaseModel):
    question: str
    answer: str

class HealthResponse(BaseModel):
    status: str
    data_records: int