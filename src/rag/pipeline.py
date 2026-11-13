from rag.chunking import chunk_pages
from rag.embeddings import generate_embeddings
from src.rag.ingestion import extract_text_from_pdf


pdf_path = "C:/Users/shasw/Downloads/CV.pdf"

pages = extract_text_from_pdf(pdf_path)

chunks = chunk_pages(pages, 1000, 200)

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

store_embeddings(chunks, embeddings, document_id)
