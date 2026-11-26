# #  we need to generate the response as well


# import ollama
# from src.config.config import config

# MODEL_NAME = config.MODEL_NAME


# def generate_answer(question: str, context: str) -> str:

#     system_prompt = """
#     You are a document-grounded question-answering assistant.

#     Your task is to answer questions using only the information
#     provided in the retrieved context.

#     Follow these rules:

#     1. Use only the provided context to answer factual questions.
#     2. Do not use external knowledge or make unsupported assumptions.
#     3. If the context contains only partial information, answer
#     the supported portion and clearly identify what is missing.
#     4. If the answer cannot be found in the context, state that
#     the information is not available in the document.
#     5. Keep answers clear, accurate, and concise.
#     6. When possible, identify the page number supporting your answer.
#     """

#     user_prompt = f"""
#     Context:
#     {context}

#     Question:
#     {question}
#     """

#     response = ollama.chat(
#         model=MODEL_NAME,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ],
#         options={"temperature": 0},
#     )

#     return response.message.content


import ollama
import logging
import time

from src.config.config import config

MODEL_NAME = config.MODEL_NAME

logger = logging.getLogger(__name__)
logger.info("generation module is working")


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

    # Measure actual wall-clock time
    start_time = time.perf_counter()

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0},
    )

    wall_time = time.perf_counter() - start_time

    # Ollama internal metrics (nanoseconds -> seconds)
    total_duration = response.total_duration / 1e9
    load_duration = response.load_duration / 1e9
    prompt_duration = response.prompt_eval_duration / 1e9
    generation_duration = response.eval_duration / 1e9

    prompt_tokens = response.prompt_eval_count
    generated_tokens = response.eval_count

    # Calculate token throughput
    prompt_speed = prompt_tokens / prompt_duration if prompt_duration > 0 else 0

    generation_speed = (
        generated_tokens / generation_duration if generation_duration > 0 else 0
    )

    logger.info(
        "Ollama Performance | Wall: %.3fs | Total: %.3fs | "
        "Load: %.3fs | Prompt: %.3fs | Generation: %.3fs",
        wall_time,
        total_duration,
        load_duration,
        prompt_duration,
        generation_duration,
    )

    logger.info(
        "Ollama Tokens | Input: %d | Output: %d | "
        "Prompt Speed: %.2f tokens/s | Generation Speed: %.2f tokens/s",
        prompt_tokens,
        generated_tokens,
        prompt_speed,
        generation_speed,
    )

    return response.message.content
