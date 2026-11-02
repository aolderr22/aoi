from langchain_openai import ChatOpenAI

def get_primary_language_model(azure_model_name, azure_project_endpoint, token_provider):
    llm = ChatOpenAI(
        model=azure_model_name,
        base_url=f"{azure_project_endpoint.rstrip('/')}/openai/v1/",
        api_key=token_provider,
        use_responses_api=True,
    )
    return llm