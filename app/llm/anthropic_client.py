from anthropic import Anthropic
from app.config import settings

class AnthropicClient:
    """
    Wrapper around the Anthropic API.

    Keeps all Claude communication in one place.
    """

    def __init__(self):
        if not settings.anthropic_api_key:
            raise ValueError(
                "Missing ANTHROPIC_API_KEY in environment variables."
            )

        self.client = Anthropic(
            api_key=settings.anthropic_api_key
        )

        self.model = settings.anthropic_model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1024,
    ) -> str:
        """
        Send a prompt to Claude and return the text response.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
        )

        return response.content[0].text