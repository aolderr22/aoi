import json

def answer_question(openai_client, model_name, employees, question):
    """Answer a question using the employee records as context."""

    employee_context = json.dumps(
        employees,
        ensure_ascii=False,
        indent=2,
    )

    response = openai_client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": (
                    "Answer questions using the supplied employee "
                    "records. If the records do not contain the "
                    "answer, say so. Do not invent employee details."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Employee records:\n{employee_context}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
    )

    return response.output_text