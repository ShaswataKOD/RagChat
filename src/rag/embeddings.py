import ollama

from src.rag.ingestion import extract_text_from_pdf
from src.rag.chunking import chunk_pages


def generate_embeddings(text: list[str]) -> list[list[float]]:
    response = ollama.embed(model="all-minilm", input=text)

    embeddings = response.embeddings

    return embeddings


if __name__ == "__main__":
    pages = extract_text_from_pdf("C:/Users/shasw/Downloads/CV.pdf")

    chunks = chunk_pages(pages, 1000, 200)

    text = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(text)

    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embeddings))
    print("Dimensions:", len(embeddings[0]))
