import ollama

from src.rag.chromaClient import upsert_chunks


def generate_embeddings(text: list[str]) -> list[list[float]]:
    response = ollama.embed(model="all-minilm", input=text)

    return response.embeddings  # type: ignore


def generate_query_embedding(query: str) -> list[float]:
    response = ollama.embed(model="all-minilm", input=query)

    return response.embeddings[0]  # type: ignore


def store_embeddings(
    chunks: list[dict], embeddings: list[list[float]], user_id: str, document_id: str
):
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count do not match")

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(f"{document_id}_chunk_{index}")

        documents.append(chunk["text"])

        metadatas.append(
            {
                "user_id": user_id,
                "document_id": document_id,
                "chunk_index": index,
                "page_number": chunk["page_number"],
            }
        )

    result = upsert_chunks(
        ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas
    )

    return result
