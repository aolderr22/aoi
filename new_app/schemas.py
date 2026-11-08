from pydantic import (BaseModel, Field)
from typing import Literal

OverlapLevel = Literal["None", "Weak", "Moderate", "Strong"]
SkillClassification = Literal["Low", "Medium", "High"]

SCORE_MAP = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

class SkillRelationship(BaseModel):
    skill_1: str
    skill_2: str

    overlap_level: OverlapLevel = Field(
        description="The degree of technical or conceptual overlap between the two skills."
    )

    shared_concepts: list[str] = Field(
        description="Technical concepts, technologies, or knowledge shared by the two skills."
    )

    transferable_knowledge: str = Field(
        description="Explain what knowledge of one skill could transfer to the other."
    )

    limitations: str = Field(
        description="Explain what knowledge of one skill does not establish about proficiency in the other."
    )


class SkillSimilarityReport(BaseModel):
    relationships: list[SkillRelationship] = Field(
        description="Relationships identified between the supplied skills."
    )

class TaskEmployeeCandidate(BaseModel):
    """
        This class is designed for evaluating a particular skill for an individual employee. 
        `Low` means limited opportunity; `High` means significant opportunity.
    """
    learning_opportunity: SkillClassification= Field(
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