from app.llm.anthropic_client import AnthropicClient
from app.config import settings

print(settings.anthropic_model)

client = AnthropicClient()

response = client.generate(
    system_prompt="You are a helpful assistant.",
    user_prompt="Explain PyTorch in two sentences."
)

print(response)