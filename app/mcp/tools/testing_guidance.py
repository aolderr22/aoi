from app.llm.anthropic_client import AnthropicClient


class TestingGuidanceTool:
    """
    Uses an LLM to generate software testing scenarios
    from a user story.
    """

    def __init__(self):
        self.client = AnthropicClient()

    def generate_scenarios(
        self,
        title: str,
        description: str,
        acceptance_criteria: str,
    ) -> str:

        response = self.client.generate(
            system_prompt="""
                You are a senior software QA engineer.

                Your job is to analyze user stories and suggest
                practical testing scenarios.

                Think about:
                - happy paths
                - edge cases
                - invalid inputs
                - regression risks
                - performance concerns
                - security concerns
                """,

                            user_prompt=f"""
                User Story:

                Title:
                {title}

                Description:
                {description}

                Acceptance Criteria:
                {acceptance_criteria}


                Generate a concise list of testing scenarios.
                Return bullet points only.
                """,
        )

        return response