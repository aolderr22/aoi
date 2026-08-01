from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    """
    Application configuration.

    All environment variables are loaded once and exposed through
    this immutable dataclass.
    """

    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Anthropic model
    anthropic_model: str = os.getenv(
        "ANTHROPIC_MODEL",
        "claude-sonnet-4-20250514"
    )

    # Embedding model
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2"
    )

    # Vector database directory
    vector_db_path: str = os.getenv(
        "VECTOR_DB_PATH",
        "./data/vector_store"
    )

    # Documents directory
    documents_path: str = os.getenv(
        "DOCUMENTS_PATH",
        "./data/documents"
    )

    # Number of retrieved documents
    top_k: int = int(
        os.getenv("TOP_K", "5")
    )

settings = Settings()