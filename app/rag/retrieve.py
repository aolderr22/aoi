from app.rag.embeddings import EmbeddingGenerator
from app.rag.vector_store import VectorStore

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
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve relevant user stories.
        """

        query_embedding = self.embedding_generator.embed_query(
            query
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        stories = []

        for index, document in enumerate(
            results["documents"][0]
        ):
            stories.append(
                {
                    "document": document,
                    "metadata": results["metadatas"][0][index],
                    "distance": results["distances"][0][index],
                }
            )

        return stories