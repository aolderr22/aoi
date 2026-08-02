from app.models.user_story import UserStory
from app.rag.embeddings import EmbeddingGenerator
from app.rag.vector_store import VectorStore

class IngestPipeline:
    """
    Pipeline for converting UserStory objects into
    searchable vector documents.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()

    def _create_document(self, story: UserStory) -> str:
        """
        Converts a UserStory into text for embedding.

        The embedding model only understands text, so we combine
        the important fields into a searchable document.
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

    def ingest(
        self,
        stories: list[UserStory]
    ) -> None:
        """
        Stores UserStories in the vector database.
        """

        documents = []
        embeddings = []
        ids = []
        metadata = []

        for index, story in enumerate(stories):

            document = self._create_document(story)
            documents.append(document)

            ids.append(
                f"story-{index}"
            )

            metadata.append(
                {
                    "title": story.title,
                    "story_url": story.story_url,
                    "feature": story.feature,
                    "priority": story.priority,
                    "status": story.status,
                }
            )

        embeddings = self.embedding_generator.embed_documents(
            documents
        )

        self.vector_store.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata,
        )