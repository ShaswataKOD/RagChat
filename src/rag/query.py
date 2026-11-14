# # here we are having all the query for similarity searching

# from src.rag.embeddings import generate_query_embedding
# from src.rag.chromaClient import collection

# # example query
# query = "What is supervised learning?"

# query_embedding = generate_query_embedding(query)


# def search_similar_chunks(
#     query_embedding: list[float], user_id: str, document_id: str, n_results: int = 3
# ):
#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=n_results,
#         where={"$and": [{"user_id": user_id}, {"document_id": document_id}]},
#     )

#     return results


# if __name__ == "__main__":
#     print(search_similar_chunks(query_embedding, "0", "0", 3))


from src.rag.embeddings import generate_query_embedding
from src.rag.chromaClient import query_chunks, get_collection_count


def search_similar_chunks(query: str, n_results: int = 3):
    query_embedding = generate_query_embedding(query)

    results = query_chunks(query_embedding=query_embedding, n_results=n_results)

    return results


if __name__ == "__main__":
    print("Collection count:", get_collection_count())

    query = "What is supervised learning?"

    results = search_similar_chunks(query, 3)

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    for index, document in enumerate(documents):
        print(f"\n--- Result {index + 1} ---")
        print("Distance:", distances[index])
        print("Metadata:", metadatas[index])
        print("Content:", document)
