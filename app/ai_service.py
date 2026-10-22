import json

def answer_question(openai_client, model_name, characters, question):
    """Answer a question using the JSON data as model context."""

    character_context = json.dumps(
        characters,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
        You are a question-answering assistant.
        
        Answer the user's question using only the supplied JSON data.
        If the data does not contain enough information, say so.
        Do not invent character details.
        
        JSON DATA:
        {character_context}
        
        USER QUESTION:
        {question}
        """

    response = openai_client.responses.create(
        model=model_name,
        input=prompt,
    )

    return response.output_text