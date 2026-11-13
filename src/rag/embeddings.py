from typing import cast

import ollama

from src.rag.ingestion import extract_text_from_pdf
from src.rag.chunking import chunk_pages
from src.rag.chromaClient import collection
from chromadb.api.types import Embeddings


def generate_embeddings(text: list[str]) -> list[list[float]]:
    response = ollama.embed(model="all-minilm", input=text)

    embeddings = response.embeddings

    return embeddings  # pyright: ignore[reportReturnType]


def store_embeddings(
    chunks: list[dict], embeddings: list[list[float]], user_id: str, document_id: str
):
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count do not match")

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        # Generate a unique ID for every chunk
        ids.append(f"{document_id}_chunk_{index}")

        # Store the original chunk text
        documents.append(chunk["text"])

        # Store chunk metadata
        metadatas.append(
            {
                "user_id": user_id,
                "document_id": document_id,
                "chunk_index": index,
                "page_number": chunk["page_number"],
            }
        )

    # Save everything in ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=cast(Embeddings, embeddings),
        metadatas=metadatas,
    )

    print(f"Successfully stored {len(ids)} chunks!")


def generate_query_embedding(query: str) -> list[float]:
    response = ollama.embed(model="all-minilm", input=query)

    return response.embeddings[0]  # pyright: ignore[reportReturnType]


query = "What is supervised learning?"

query_embedding = generate_query_embedding(query)

print("Query:", query)
print("Embedding dimensions:", len(query_embedding))
print("First 5 values:", query_embedding[:5])
# if __name__ == "__main__":
#     pages = extract_text_from_pdf("C:/Users/shasw/Downloads/CV.pdf")

#     chunks = chunk_pages(pages, 1000, 200)

#     text = [chunk["text"] for chunk in chunks]

#     embeddings = generate_embeddings(text)

#     print("Total chunks:", len(chunks))
#     print("Total embeddings:", len(embeddings))
#     print("Dimensions:", len(embeddings[0]))
