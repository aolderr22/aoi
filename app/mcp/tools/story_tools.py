from app.rag.retrieve import Retriever

class StoryTools:
    """
    MCP tools related to user stories.
    """

    def __init__(self):
        self.retriever = Retriever()

    def search_user_stories(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search for user stories related to an engineer's question.
        """

        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )