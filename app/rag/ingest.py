from data.documents.user_stories import USER_STORIES

from app.rag.embeddings import EmbeddingGenerator
from app.rag.vector_store import VectorStore


def story_to_text(story):
    """
    Convert a UserStory object into searchable text.
    """

    return f"""
Title:
{story.title}

Description:
{story.description}

Acceptance Criteria:
{story.acceptance_criteria}

Feature:
{story.feature}

Priority:
{story.priority}

Status:
{story.status}
"""


def ingest():
    """
    Load user stories into ChromaDB.
    """

    embedding_generator = EmbeddingGenerator()
    vector_store = VectorStore()

    # Delete old vectors
    vector_store.delete_all()

    documents = []
    ids = []
    metadatas = []

    for index, story in enumerate(USER_STORIES):

        documents.append(
            story_to_text(story)
        )

        ids.append(
            f"story_{index}"
        )

        metadatas.append(
            {
                "title": story.title,
                "story_url": story.story_url,
                "feature": story.feature,
                "priority": story.priority,
                "status": story.status,
                "acceptance_criteria": story.acceptance_criteria,
            }
        )

    embeddings = embedding_generator.embed_documents(
        documents
    )

    vector_store.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"Ingested {len(documents)} user stories."
    )


if __name__ == "__main__":
    ingest()