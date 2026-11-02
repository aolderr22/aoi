from langchain.agents import create_agent
from prompts import SKILL_MATCHING_AGENT_SYSTEM_PROMPT
from schemas import TaskEmployeeCandidate

def get_skill_matching_agent(llm):
    skill_matching_agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SKILL_MATCHING_AGENT_SYSTEM_PROMPT,
        response_format=TaskEmployeeCandidate
    )

    return skill_matching_agent