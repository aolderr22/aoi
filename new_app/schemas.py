from pydantic import BaseModel, Field
from typing import Literal

SkillClassification = Literal["Low", "Medium", "High"]

SCORE_MAP = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

class TaskEmployeeCandidate(BaseModel):
    learning_opportunity: SkillClassification = Field(
        description="Employee's learning opportunity."
    )

    leadership_capability: SkillClassification = Field(
        description="Employee's technical leadership and mentoring capability."
    )

    learning_explanation: str = Field(
        description="Brief explanation supporting the learning opportunity classification."
    )

    leadership_explanation: str = Field(
        description="Brief explanation supporting the leadership capability classification."
    )