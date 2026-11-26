import time
import logging

from src.rag.reranker import use_reranker
from src.rag.generation import generate_answer
from src.rag.embeddings import generate_query_embedding
from src.rag.chromaClient import query_chunks

logger = logging.getLogger(__name__)


def search_similar_chunks(
    query: str,
    user_id: str,
    document_id: str,
    n_results: int = 15,
    reranker: bool = False,
    top_n: int = 5,
):
    # Step 1: Query embedding
    start = time.perf_counter()

    query_embedding = generate_query_embedding(query)

    embedding_time = time.perf_counter() - start

    # Step 2: Construct metadata filter
    where = {
        "$and": [
            {"user_id": user_id},
            {"document_id": document_id},
        ]
    }

    # Step 3: ChromaDB retrieval
    start = time.perf_counter()

    results = query_chunks(
        query_embedding=query_embedding,
        n_results=n_results,
        where=where,
    )

    retrieval_time = time.perf_counter() - start

    if reranker:
        start = time.perf_counter()

        result_after_reranking = use_reranker(query=query, results=results, top_n=top_n)

    reranking_time = time.perf_counter() - start

    logger.info(
        "RAG Retrieval | Embedding: %.3fs | ChromaDB: %.3fs | Reranking: %.3fs",
        embedding_time,
        retrieval_time,
        reranking_time,
    )

    return results


def ask_question(
    question: str,
    user_id: str,
    document_id: str,
    n_results: int = 3,
):
    total_start = time.perf_counter()

    # Step 1: Retrieval
    start = time.perf_counter()

    results = search_similar_chunks(
        query=question,
        user_id=user_id,
        document_id=document_id,
        n_results=n_results,
    )

    retrieval_pipeline_time = time.perf_counter() - start

    # Step 2: Extract documents
    documents = results.get("documents")

    if not documents or not documents[0]:
        raise ValueError("No relevant chunks found.")

    documents = documents[0]

    metadatas = results.get("metadatas")
    metadatas = metadatas[0] if metadatas else []

    # Step 3: Prepare context
    start = time.perf_counter()

    context_parts = []

    for index, text in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        page = metadata.get("page_number", "Unknown")

        context_parts.append(f"[Page {page}]\n{text}")

    context = "\n\n".join(context_parts)

    context_time = time.perf_counter() - start

    # Step 4: Generate answer
    start = time.perf_counter()

    answer = generate_answer(question, context)

    generation_time = time.perf_counter() - start

    total_time = time.perf_counter() - total_start

    logger.info(
        "RAG Performance | Retrieval: %.3fs | "
        "Context: %.3fs | Generation: %.3fs | Total: %.3fs",
        retrieval_pipeline_time,
        context_time,
        generation_time,
        total_time,
    )

    return answer


def ask_question_with_context(
    question: str, user_id: str, document_id: str, n_results: int = 3
):
    results = search_similar_chunks(
        query=question, user_id=user_id, document_id=document_id, n_results=n_results
    )

    documents = results.get("documents")
    metadatas = results.get("metadatas")

    if not documents or not documents[0]:
        return {
            "answer": "No relevant information found in this document.",
            "contexts": [],
        }

    documents = documents[0]
    metadatas = metadatas[0] if metadatas else []

    context_parts = []

    for index, chunk in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        page = metadata.get("page_number", "Unknown")

        context_parts.append(f"[Page {page}]\n{chunk}")

    context = "\n\n".join(context_parts)

    answer = generate_answer(question, context)

    return {"answer": answer, "contexts": context_parts}
