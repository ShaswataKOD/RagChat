from src.rag.generation import generate_answer
from src.rag.embeddings import generate_query_embedding
from src.rag.chromaClient import query_chunks, get_collection_count


def search_similar_chunks(query: str, n_results: int = 3):
    query_embedding = generate_query_embedding(query)

    results = query_chunks(query_embedding=query_embedding, n_results=n_results)

    return results


def ask_question(question: str):

    # Step 1: Retrieve relevant chunks
    results = search_similar_chunks(question)

    # Step 2: Extract retrieved text
    documents = results["documents"][0]

    # Step 3: Construct context
    context = "\n\n".join(documents)

    # Step 4: Generate answer
    answer = generate_answer(question, context)

    return answer


if __name__ == "__main__":
    question = "What skills and technologies are mentioned in my CV?"

    answer = ask_question(question)

    print("\nQuestion:", question)
    print("\nAnswer:", answer)
