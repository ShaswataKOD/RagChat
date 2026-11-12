pages = extract_text_from_pdf(pdf_path)

chunks = chunk_pages(pages, 1000, 200)

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

store_embeddings(chunks, embeddings, user_id, document_id)
