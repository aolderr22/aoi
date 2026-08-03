import chromadb
from app.config import settings


class VectorStore:
    """
    Wrapper around ChromaDB.

    Responsible only for storing and retrieving vector embeddings.
    """

    COLLECTION_NAME = "user_stories"

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_path
        )

    def _collection(self):
        """
        Always fetch the latest collection.
        """
        return self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:

        self._collection().add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict:

        return self._collection().query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def delete_all(self) -> None:
        """
        Recreate the collection from scratch.
        """

        try:
            self.client.delete_collection(self.COLLECTION_NAME)
        except Exception:
            pass

        self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )