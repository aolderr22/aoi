from prompts import (get_skill_task_similarity_prompt, get_skill_task_matching_prompt)
from schemas import (SCORE_MAP, TaskEmployeeCandidate)

def match_task_to_skills(
    task_id: int,
    skills: list[str],
    employee: dict,
    skill_similarity_investigator_agent,
    skill_matching_agent
) -> tuple[TaskEmployeeCandidate, int, int]:

    # STEP 1: Investigate skill relationships
    try:
        required_skill_names = {
            skill.strip().casefold()
            for skill in skills
        }
    
        employee_skills_for_similarity = {
            skill: proficiency
            for skill, proficiency in employee["skill_map"].items()
            if skill.strip().casefold() not in required_skill_names
        }
        
        similarity_prompt = get_skill_task_similarity_prompt(skills, employee_skills_for_similarity)

        similarity_result = skill_similarity_investigator_agent.invoke({
            "messages": [
                {"role": "user", "content": similarity_prompt}
            ]
        })

        similarity_report = similarity_result["structured_response"]

        similarity_findings = similarity_report.model_dump_json(indent=2)

    except Exception as e:
        print(f"Skill similarity investigation failed: {e}")

        # Continue matching without similarity findings.
        similarity_findings = (
            "No similarity findings are available. "
            "Evaluate the employee using the available skill map "
            "and demonstrated proficiency."
        )

    # STEP 2: Evaluate employee against task requirements
    skill_matching_prompt = get_skill_task_matching_prompt(skills, employee, similarity_findings)

    try:
        result = skill_matching_agent.invoke({
            "messages": [
                {"role": "user", "content": skill_matching_prompt}
            ]
        })

        structured_response = result["structured_response"]

        print("Structured response:", structured_response)

        return (
            structured_response,
            task_id,
            employee["id"]
        )

    except Exception as e:
        print(f"Skill matching agent failed: {e}")

        return (
            TaskEmployeeCandidate(
                learning_opportunity="Medium",
                leadership_capability="Medium",
                learning_explanation="Unable to determine learning opportunity.",
                leadership_explanation="Unable to determine leadership capability."
            ),
            task_id,
            employee["id"]
        )

def rank_employee_task_matches(task_data, employee_data, skill_similarity_investigator_agent, skill_matching_agent):
    skill_matches = []
    for task in task_data:
        skills = ", ".join(task['required_skills'])
        for employee in employee_data:
            skill_match = match_task_to_skills(task['id'], skills, employee, skill_similarity_investigator_agent, skill_matching_agent)
            skill_matches.append(skill_match)

    learning_ranked = sorted(
        skill_matches,
        key=lambda x: SCORE_MAP[x[0].learning_opportunity]
    )

    leadership_ranked = sorted(
        skill_matches,
        key=lambda x: SCORE_MAP[x[0].leadership_capability],
    )

    return (learning_ranked, leadership_ranked)