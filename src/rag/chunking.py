# so we are using recusrsive Text Splitters for chunking our texts
# splitting won't have the overlapping page cotext

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.ingestion import extract_text_from_pdf


def chunk_pages(pages: list[dict], chunk_size: int, chunk_overlapp: int) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk size is negative")

    if chunk_size < 0 or chunk_overlapp > chunk_size:
        raise ValueError(
            "chunk overlap must be non-negative and can't be greater thn chunk size"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlapp,
        separators=["\n\n", "\n", ",", ""],
    )

    chunks = []

    for page in pages:
        page_number = page["page_number"]
        text = page["text"].strip()

        if not text:
            continue

        page_chunks = splitter.split_text(text)

        for index, chunk_text in enumerate(page_chunks):
            chunks.append(
                {"page_number": page_number, "chunk_index": index, "text": chunk_text}
            )
    return chunks
