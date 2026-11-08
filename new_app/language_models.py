from langchain_openai import (ChatOpenAI, OpenAIEmbeddings)

def get_primary_language_model(azure_foundry_model_name, azure_foundry_project_endpoint, token_provider):
    llm = ChatOpenAI(
        model=azure_foundry_model_name,
        base_url=f"{azure_foundry_project_endpoint.rstrip('/')}/openai/v1/",
        api_key=token_provider,
        use_responses_api=True,
    )
    return llm

def get_embeddings_model(azure_foundry_embedding_model_name, azure_foundry_model_endpoint, token_provider):
    embeddings_model = OpenAIEmbeddings(
        model=azure_foundry_embedding_model_name,
        base_url=f"{azure_foundry_model_endpoint.rstrip('/')}/openai/v1/",
        api_key=token_provider,
    )
    return embeddings_model