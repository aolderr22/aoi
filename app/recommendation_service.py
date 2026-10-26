import json
import numpy as np
from langchain_core.runnables import RunnableLambda

PROFICIENCY_MULTIPLIERS = {
    "productive": {
        "novice": 0.5,
        "intermediate": 1,
        "advanced": 1.5,
        "expert": 2,
    },
    "knowledge_transfer": {
        "novice": 2,
        "intermediate": 1.5,
        "advanced": 1,
        "expert": 0.5,
    },
}

def _to_dict(record):
    if hasattr(record, "model_dump"):
        return record.model_dump()
    return record

def _employee_to_text(employee):
    employee = _to_dict(employee)

    skills = employee.get("skill_map", {})
    skill_text = ", ".join(
        f"{skill}: {level}"
        for skill, level in skills.items()
    )

    return (
        f"Employee: {employee.get('name', '')}. "
        f"Position: {employee.get('position', '')}. "
        f"Skills and proficiency: {skill_text}."
    )

def _task_to_text(task):
    if isinstance(task, str):
        return task

    task = _to_dict(task)

    title = task.get("title", "")
    description = task.get("description", "")
    skills = task.get("required_skills", [])

    return (
        f"Task: {title}. "
        f"Description: {description}. "
        f"Required skills: {', '.join(skills)}."
    )

def recommend_employee(openai_client, model_name, employees, task):
    print("employees", employees)
    """Use a two-step LangChain pipeline to select the best employee."""

    employee_records = [
        employee.model_dump()
        if hasattr(employee, "model_dump")
        else employee
        for employee in employees
    ]

    def build_prompt(inputs):
        return f"""
            You are an employee-task matching assistant.
            
            Select the single best employee for the task using only the
            provided employee records.
            
            Consider:
            - Relevant skills and their proficiency levels.
            - The employee's position.
            - How closely their skills match the task.
            
            Do not invent skills or qualifications.
            If no employee is a strong match, select the closest match
            and explain the limitations.
            
            Return ONLY valid JSON with this structure:
            {{
              "employee_id": 0,
              "reason": "Explanation of why this employee is the best match.",
              "matched_skills": ["python", "sql"]
            }}
            
            TASK:
            {inputs["task"]}
            
            EMPLOYEES:
            {json.dumps(inputs["employees"], ensure_ascii=False, indent=2)}
            """

    def call_model(prompt):
        response = openai_client.responses.create(
            model=model_name,
            input=prompt,
        )
        return response.output_text

    chain = RunnableLambda(build_prompt) | RunnableLambda(call_model)

    result = json.loads(
        chain.invoke({
            "task": task,
            "employees": employee_records,
        })
    )

    employee_id = int(result["employee_id"])

    selected_employee = next(
        (
            employee
            for employee in employee_records
            if employee["id"] == employee_id
        ),
        None,
    )

    if selected_employee is None:
        raise ValueError("The model returned an unknown employee ID.")

    return {
        "employee": selected_employee,
        "reason": result["reason"],
        "matched_skills": result["matched_skills"],
    }

def mapEmployeesToTasks(embedding_client, embedding_model_name, employees, tasks, mode="productive"):
    if not employees or not tasks:
        return {}

    mapping = {}
    employee_texts = [
        _employee_to_text(employee)
        for employee in employees
    ]
    task_texts = [
        _task_to_text(task)
        for task in tasks
    ]

    # Generate numeric embeddings using your resource-level client.
    employee_response = embedding_client.embeddings.create(
        model=embedding_model_name,
        input=employee_texts,
    )
    task_response = embedding_client.embeddings.create(
        model=embedding_model_name,
        input=task_texts,
    )

    employee_vectors = np.asarray([
        item.embedding
        for item in sorted(
            employee_response.data,
            key=lambda item: item.index,
        )
    ], dtype=np.float32)

    task_vectors = np.asarray([
        item.embedding
        for item in sorted(
            task_response.data,
            key=lambda item: item.index,
        )
    ], dtype=np.float32)

    # Normalize vectors so their dot products equal cosine similarities.
    employee_norms = np.linalg.norm(
        employee_vectors, axis=1, keepdims=True
    )
    task_norms = np.linalg.norm(
        task_vectors, axis=1, keepdims=True
    )

    if np.any(employee_norms == 0) or np.any(task_norms == 0):
        raise ValueError("An embedding contains a zero vector.")

    employee_vectors = employee_vectors / employee_norms
    task_vectors = task_vectors / task_norms
    
    return mapping