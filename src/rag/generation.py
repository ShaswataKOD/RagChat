#  we need to generate the response as well


import ollama

MODEL_NAME = "llama3.2:1b"


def generate_answer(question: str, context: str) -> str:

    system_prompt = """
    You are a document question-answering assistant.

    Answer the user's question using only the provided context.

    If the context does not contain enough information to answer,
    clearly say that the information is not available in the document.

    Do not invent facts or make unsupported assumptions.
    Keep your answers clear and easy to understand.
    """

    user_prompt = f"""
    Context:
    {context}

    Question:
    {question}
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.message.content
