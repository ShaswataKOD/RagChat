from google import genai
from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings

from src.config.config import config

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)


gemini_client = genai.Client(api_key=config.API_KEY)

evaluator_llm = llm_factory(
    model=config.GEMINI_MODEL, provider="google", client=gemini_client
)

evaluator_embeddings = GoogleEmbeddings(
    client=gemini_client, model="gemini-embedding-001"
)


faithfulness = Faithfulness(llm=evaluator_llm)

answer_relevancy = AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)

context_precision = ContextPrecision(llm=evaluator_llm)

context_recall = ContextRecall(llm=evaluator_llm)


METRICS = {
    "faithfulness": faithfulness,
    "answer_relevancy": answer_relevancy,
    "context_precision": context_precision,
    "context_recall": context_recall,
}
