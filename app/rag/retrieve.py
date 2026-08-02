from app.rag.embeddings import EmbeddingGenerator
from app.rag.vector_store import VectorStore
from app.config import settings

class Retriever:
    """
    Retrieves relevant user stories from the vector database.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[dict]:
        """
        Retrieve the most relevant user stories.

        Returns raw search results from the vector store.
        A higher-level component will convert these into
        final responses.
        """

        if top_k is None:
            top_k = settings.top_k

        query_embedding = self.embedding_generator.embed_query(
            query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return self._format_results(results)

    def _format_results(
        self,
        results: dict,
    ) -> list[dict]:
        """
        Convert Chroma's response format into
        a cleaner structure.
        """

        formatted = []

        documents = results.get("documents", [[]])[0]
        metadata = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for document, meta, distance in zip(
            documents,
            metadata,
            distances,
        ):
            formatted.append(
                {
                    "document": document,
                    "metadata": meta,
                    "similarity_score": distance,
                }
            )

        return formatted