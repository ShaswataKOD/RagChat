from pathlib import Path

from src.rag.chunking import chunk_pages
from src.rag.embeddings import generate_embeddings, store_embeddings
from src.rag.ingestion import extract_text_from_pdf


def ingest_document(file_path: str, user_id: str, document_id: str) -> dict:

    # Step 1: Extract PDF text
    pages = extract_text_from_pdf(file_path)

    # Step 2: Generate chunks
    chunks = chunk_pages(pages, chunk_size=1000, chunk_overlapp=200)

    if not chunks:
        raise ValueError("No chunks were generated from the PDF.")

    # Step 3: Generate embeddings
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    # Step 4: Store embeddings with metadata
    result = store_embeddings(chunks, embeddings, user_id, document_id)

    return {
        "document_id": document_id,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "status": "completed",
        "storage_result": result,
    }
