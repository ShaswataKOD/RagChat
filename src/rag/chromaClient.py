import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)


collection = client.get_or_create_collection(
    name="document_chunks", metadata={"hnsw:space": "cosine"}
)

print("Collection:", collection.name)
print("Collection count:", collection.count())