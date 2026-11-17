#  we need to generate the response as well


import ollama
from src.config.config import config

MODEL_NAME = config.MODEL_NAME


def generate_answer(question: str, context: str) -> str:

    system_prompt = """
    You are a document-grounded question-answering assistant.

    Your task is to answer questions using only the information
    provided in the retrieved context.

    Follow these rules:

    1. Use only the provided context to answer factual questions.
    2. Do not use external knowledge or make unsupported assumptions.
    3. If the context contains only partial information, answer
    the supported portion and clearly identify what is missing.
    4. If the answer cannot be found in the context, state that
    the information is not available in the document.
    5. Keep answers clear, accurate, and concise.
    6. When possible, identify the page number supporting your answer.
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
        options={"temperature": 0},
    )

    return response.message.content
