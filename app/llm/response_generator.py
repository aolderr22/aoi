from app.llm.anthropic_client import AnthropicClient
from app.llm.prompts import SYSTEM_PROMPT

from app.rag.retrieve import Retriever
from app.models.response import Response

from app.mcp.tools.testing_guidance import TestingGuidanceTool


class ResponseGenerator:
    """
    Generates final AI responses using retrieved user stories,
    Anthropic, and supporting tools.
    """

    def __init__(self):
        self.client = AnthropicClient()
        self.retriever = Retriever()
        self.testing_tool = TestingGuidanceTool()

    def generate(
        self,
        question: str,
    ) -> Response:
        """
        Retrieve relevant stories, generate implementation guidance,
        and generate testing scenarios.
        """

        stories = self.retriever.retrieve(
            query=question,
            top_k=3,
        )

        if not stories:
            return Response(
                story_title="No matching story found",
                story_url="",
                feature="",
                priority="",
                acceptance_criteria="",
                notes="No stories matched the request.",
                testing_scenarios="",
            )

        best_story = stories[0]

        metadata = best_story["metadata"]

        notes = self.client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=f"""
Engineer request:

{question}


Recommended user story:

{best_story["document"]}


Explain:

1. Why this story is the best choice.
2. Where the engineer should begin.
3. Important implementation considerations.
""",
        )

        testing_scenarios = self.testing_tool.generate_scenarios(
            title=metadata["title"],
            description=best_story["document"],
            acceptance_criteria=metadata.get(
                "acceptance_criteria",
                "",
            ),
        )

        return Response(
            story_title=metadata["title"],
            story_url=metadata["story_url"],
            feature=metadata["feature"],
            priority=metadata["priority"],
            acceptance_criteria=metadata.get(
                "acceptance_criteria",
                "",
            ),
            notes=notes,
            testing_scenarios=testing_scenarios,
        )