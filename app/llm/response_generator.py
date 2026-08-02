from app.llm.anthropic_client import AnthropicClient
from app.llm.prompts import SYSTEM_PROMPT

from app.rag.retrieve import Retriever
from app.models.response import Response

class ResponseGenerator:
    """
    Generates final AI responses using retrieved user stories
    and the Anthropic LLM.
    """

    def __init__(self):
        self.client = AnthropicClient()
        self.retriever = Retriever()

    def generate(
        self,
        question: str,
    ) -> Response:
        """
        Retrieve relevant stories and ask Claude
        to recommend the best task.
        """

        stories = self.retriever.retrieve(
            query=question,
            top_k=3,
        )

        context = self._format_context(
            stories
        )

        answer = self.client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=f"""
Engineer request:

{question}


Available user stories:

{context}


Choose the most appropriate story for the engineer.
Return:

Story Title:
Acceptance Criteria:
Notes:
""",
        )

        return self._parse_response(
            answer
        )

    def _format_context(
        self,
        stories: list[dict],
    ) -> str:
        """
        Convert retrieved stories into LLM context.
        """

        formatted = []

        for story in stories:
            formatted.append(
                story["document"]
            )

        return "\n\n".join(formatted)

    def _parse_response(
        self,
        text: str,
    ) -> Response:
        """
        Temporary parser.

        Later we can use structured output.
        """

        return Response(
            story_title=text,
            acceptance_criteria="",
            notes="",
        )