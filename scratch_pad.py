import numpy as np
from scipy.optimize import linear_sum_assignment

PROFICIENCY_MULTIPLIERS = {
    "productive": {
        "novice": 0.70,
        "intermediate": 0.90,
        "advanced": 1.10,
        "expert": 1.20,
    },
    "knowledge_transfer": {
        "novice": 1.30,
        "intermediate": 1.10,
        "advanced": 0.90,
        "expert": 0.70,
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

def _proficiency_multiplier(employee, task, mode):
    employee = _to_dict(employee)
    task = _to_dict(task) if not isinstance(task, str) else {}

    skill_map = {
        skill.lower(): level.lower()
        for skill, level in employee.get("skill_map", {}).items()
    }

    required_skills = task.get("required_skills", [])

    # Apply proficiency adjustments to skills required by the task.
    relevant_levels = [
        skill_map[skill.lower()]
        for skill in required_skills
        if skill.lower() in skill_map
    ]

    # Without explicit required skills, use semantic similarity alone.
    if not relevant_levels:
        return 1.0

    multipliers = PROFICIENCY_MULTIPLIERS[mode]

    return float(np.mean([
        multipliers.get(level, 1.0)
        for level in relevant_levels
    ]))

def mapEmployeesToTasks(
    embedding_client,
    embedding_model_name,
    employees,
    tasks,
    mode="productive",
):
    """
    Assign employees to unique tasks using numeric embeddings.

    Each employee and task is embedded as a numeric vector.
    Cosine similarity measures semantic relevance.
    Proficiency multipliers adjust scores by mode.
    The Hungarian algorithm finds the best overall assignment.

    Returns a dictionary keyed by task ID, or task index if no ID exists.
    """

    if mode not in PROFICIENCY_MULTIPLIERS:
        raise ValueError(
            "mode must be 'productive' or 'knowledge_transfer'"
        )

    if not employees or not tasks:
        return {}

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

    # Shape: number of employees x number of tasks.
    similarity_matrix = employee_vectors @ task_vectors.T

    # Apply mode-specific proficiency adjustments.
    score_matrix = similarity_matrix.copy()

    for employee_index, employee in enumerate(employees):
        for task_index, task in enumerate(tasks):
            multiplier = _proficiency_multiplier(
                employee, task, mode
            )
            score_matrix[employee_index, task_index] *= multiplier

    # Find a globally optimal one-to-one assignment.
    employee_indices, task_indices = linear_sum_assignment(
        -score_matrix
    )

    mapping = {}

    for employee_index, task_index in zip(
        employee_indices, task_indices
    ):
        employee = _to_dict(employees[employee_index])
        task = _to_dict(tasks[task_index])

        task_key = (
            task.get("id", task_index)
            if isinstance(task, dict)
            else task_index
        )

        mapping[task_key] = {
            "employee": employee,
            "task": task,
            "cosine_similarity": float(
                similarity_matrix[employee_index, task_index]
            ),
            "adjusted_score": float(
                score_matrix[employee_index, task_index]
            ),
            "mode": mode,
        }

    return mapping


tasks = [
    {
        "id": "task-001",
        "title": "Build a Python API",
        "description": "Create an API that queries SQL data.",
        "required_skills": ["python", "sql"],
    },
    {
        "id": "task-002",
        "title": "Deploy infrastructure",
        "description": "Provision cloud resources using Pulumi.",
        "required_skills": ["pulumi", "python"],
    },
]

productive_mapping = mapEmployeesToTasks(
    embedding_client,
    embedding_model,
    employees,
    tasks,
    mode="productive",
)

learning_mapping = mapEmployeesToTasks(
    embedding_client,
    embedding_model,
    employees,
    tasks,
    mode="knowledge_transfer",
)

service = BlobServiceClient(
    account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
    credential=credential,
)

container_name = os.environ["AZURE_STORAGE_CONTAINER_TASKS"]

container = None
try:
    container = service.create_container(name=container_name)
    print(f"Created container: {container_name}")
except ResourceExistsError:
    container = service.get_container_client(container_name)
    print(f"Container already exists: {container_name}")

# Path to your separate JSON file
json_path = Path("data/tasks.json")

# Verify the file exists
if not json_path.is_file():
    raise FileNotFoundError(
        f"Could not find {json_path.resolve()}. "
        "Check that the file is in your project's data folder."
    )

# Choose the destination name in Azure Blob Storage
blob_name = "tasks/tasks.json"

# Upload the file
blob = container.get_blob_client(blob_name)

with json_path.open("rb") as file:
    blob.upload_blob(file, overwrite=True)

print(f"Successfully uploaded {json_path.name}")
print(f"Azure blob name: {blob_name}")