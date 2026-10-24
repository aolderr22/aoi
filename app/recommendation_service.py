import json
from langchain_core.runnables import RunnableLambda

def recommend_employee(openai_client, model_name, employees, task):
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