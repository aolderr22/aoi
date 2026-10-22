from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="A question about the character data.",
    )

class AskResponse(BaseModel):
    question: str
    answer: str