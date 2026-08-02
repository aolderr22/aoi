from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
    Generates vector embeddings for documents and user queries.

    This class wraps the SentenceTransformer model so the rest of
    the application doesn't depend directly on the embedding library.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """
        Convert a list of documents into embeddings.
        """
        return self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

    def embed_query(self, query: str) -> list[float]:
        """
        Convert a single user query into an embedding.
        """
        return self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()