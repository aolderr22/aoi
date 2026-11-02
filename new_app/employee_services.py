import json
from azure.storage.blob import BlobServiceClient
from prompts import skill_matching_prompt
from schemas import (TaskEmployeeCandidate, SCORE_MAP)

def load_employee_data(credential, account_url, container_name, blob_name):
    """Download employee JSON data from Azure Blob Storage."""

    try:
        service = BlobServiceClient(
            account_url=account_url,
            credential=credential,
        )

        blob = service.get_blob_client(
            container=container_name,
            blob=blob_name,
        )

        json_bytes = blob.download_blob().readall()
        data = json.loads(json_bytes.decode("utf-8"))

        # Accept either a list or {"employees": [...]}.
        if isinstance(data, dict):
            data = data.get("employees")

        if not isinstance(data, list):
            raise ValueError(
                "Employee data must be a JSON list or an "
                "object containing an 'employees' list."
            )

        return data

    finally:
        credential.close()

def load_task_data(credential, account_url, container_name, blob_name):
    """Download task JSON data from Azure Blob Storage."""

    try:
        service = BlobServiceClient(
            account_url=account_url,
            credential=credential,
        )

        blob = service.get_blob_client(
            container=container_name,
            blob=blob_name,
        )

        json_bytes = blob.download_blob().readall()
        data = json.loads(json_bytes.decode("utf-8"))

        # Accept either a list or {"tasks": [...]}.
        if isinstance(data, dict):
            data = data.get("tasks")

        if not isinstance(data, list):
            raise ValueError(
                "Task data must be a JSON list or an "
                "object containing a 'tasks' list."
            )

        return data

    finally:
        credential.close()

def match_task_to_skills(
    task_id,
    skills,
    employee,
    skill_matching_agent
) -> tuple[TaskEmployeeCandidate, int, int]:

    try:
        human_message = skill_matching_prompt.format_messages(
            task_id=task_id,
            required_skills=skills,
            employee_id=employee["id"],
            employee_skills=employee["skill_map"]
        )

        result = skill_matching_agent.invoke({
            "messages": human_message
        })

        return (
            result["structured_response"],
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

def rank_employee_task_matches(task_data, employee_data, skill_matching_agent):
    skill_matches = []
    for task in task_data:
        skills = ", ".join(task['required_skills'])
        for employee in employee_data:
            skill_match = match_task_to_skills(task['id'], skills, employee, skill_matching_agent)
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