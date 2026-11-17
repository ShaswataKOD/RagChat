from src.rag.generation import generate_answer
from src.rag.embeddings import generate_query_embedding
from src.rag.chromaClient import query_chunks


def search_similar_chunks(
    query: str,
    user_id: str,
    document_id: str,
    n_results: int = 3,
):
    # Step 1: Generate query embedding
    query_embedding = generate_query_embedding(query)

    # Step 2: Construct metadata filter
    where = {
        "$and": [
            {"user_id": user_id},
            {"document_id": document_id},
        ]
    }

    # Step 3: Retrieve matching chunks
    results = query_chunks(
        query_embedding=query_embedding,
        n_results=n_results,
        where=where,
    )

    return results


def ask_question(question: str, user_id: str, document_id: str, n_results: int = 3):
    results = search_similar_chunks(
        query=question, user_id=user_id, document_id=document_id, n_results=n_results
    )

    documents = results.get("documents")

    if not documents or not documents[0]:
        return "No relevant information found in this document."

    documents = documents[0]

    metadatas = results.get("metadatas")

    metadatas = metadatas[0] if metadatas else []

    context_parts = []

    for index, text in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        page = metadata.get("page_number", "Unknown")

        context_parts.append(f"[Page {page}]\n{text}")

    context = "\n\n".join(context_parts)

    return generate_answer(question, context)
