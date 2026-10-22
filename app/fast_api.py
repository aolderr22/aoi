from fastapi import FastAPI, Request
from langchain_anthropic import ChatOpenAI
from langchain_core.messages import HumanMessage
import uvicorn

def build_fast_api(model_name):
    # Initialize FastAPI app
    app = FastAPI()

    # Authenticate using your existing az login
    credential = DefaultAzureCredential()

    token_provider = get_bearer_token_provider(
        credential,
        "https://ai.azure.com/.default",
    )

    openai_client = project.get_openai_client()

    # Initialize the LLM
    llm = ChatOpenAI(
        model=model_name,
        base_url=str(openai_client.base_url),
        api_key=token_provider
    )

@app.post("/get_characters")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")