from langchain.agents import create_agent
from prompts import (SKILL_MATCHING_AGENT_SYSTEM_PROMPT, SKILL_SIMILARITY_INVESTIGATOR_PROMPT)
from schemas import (TaskEmployeeCandidate, SkillSimilarityReport)

def get_skill_matching_agent(llm):
    skill_matching_agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SKILL_MATCHING_AGENT_SYSTEM_PROMPT,
        response_format=TaskEmployeeCandidate
    )
    return skill_matching_agent

def get_skill_similarity_investigator_agent(llm):
    skill_similarity_investigator_agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SKILL_SIMILARITY_INVESTIGATOR_PROMPT,
        response_format=SkillSimilarityReport
    )
    return skill_similarity_investigator_agent