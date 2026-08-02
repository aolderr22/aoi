from app.llm.anthropic_client import AnthropicClient
from app.llm.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)

from app.models.response import Response
from app.rag.retrieve import Retriever

class ResponseGenerator:
    """
    Coordinates retrieval, prompting, and LLM generation.
    """

    def __init__(self):
        self.client = AnthropicClient()
        self.retriever = Retriever()

    def generate(
        self,
        query: str,
    ) -> Response:
        """
        Generate a structured response for an engineer.
        """

        stories = self.retriever.retrieve(
            query=query
        )

        if not stories:
            return Response(
                story_title="No matching story found",
                acceptance_criteria="",
                notes=(
                    "No relevant user stories were found. "
                    "Try providing more details."
                ),
            )

        best_story = stories[0]

        context = "\n\n".join(
            [
                story["document"]
                for story in stories
            ]
        )

        user_prompt = USER_PROMPT_TEMPLATE.format(
            query=query,
            context=context,
        )

        notes = self.client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        metadata = best_story["metadata"]

        return Response(
            story_title=metadata.get(
                "title",
                "Unknown",
            ),
            acceptance_criteria=self._extract_acceptance_criteria(
                best_story["document"]
            ),
            notes=notes,
        )

    def _extract_acceptance_criteria(
        self,
        document: str,
    ) -> str:
        """
        Extract acceptance criteria from the stored document.

        Temporary implementation.
        Later this can be replaced with structured metadata.
        """

        marker = "Acceptance Criteria:"

        if marker not in document:
            return ""

        return document.split(
            marker,
            1
        )[1].split(
            "Feature:",
            1
        )[0].strip()