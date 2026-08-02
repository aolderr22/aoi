import chromadb
from app.config import settings

class VectorStore:
    """
    Wrapper around ChromaDB.

    Responsible only for storing and retrieving vector embeddings.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name="user_stories"
        )

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Add documents to the vector store.
        """

        self.collection.add(
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
        """
        Return the top matching documents.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def delete_all(self) -> None:
        """
        Deletes every document from the collection.

        Very useful while developing.
        """

        self.client.delete_collection("user_stories")

        self.collection = self.client.get_or_create_collection(
            name="user_stories"
        )