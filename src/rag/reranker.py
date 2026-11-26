# we are to generate the reranker for getting better context precision result

# let's initialise the cohere client

import cohere
import os
from src.config.config import config

cohere = cohere.ClientV2(api_key=config.COHERE_API_KEY)


def use_reranker(query: str, top_n: int, results):

    documents = results["documents"][0]

    if not documents:
        return results

    response = cohere.rerank(
        model="rerank-v5.0-pro",
        query=query,
        documents=documents,
        top_n=min(top_n, len(documents)),
    )

    ranked = {
        "ids": [],
        "documents": [],
        "metadatas": [],
        "distances": [],
        "relevance_scores": [],
    }

    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for item in response.results:
        index = item.index

        ranked["ids"].append(ids[index])
        ranked["documents"].append(documents[index])
        ranked["metadatas"].append(metadatas[index])
        ranked["distances"].append(distances[index])
        ranked["relevance_scores"].append(item.relevance_score)

    # Preserve ChromaDB's outer list structure.
    return {
        "ids": [ranked["ids"]],
        "documents": [ranked["documents"]],
        "metadatas": [ranked["metadatas"]],
        "distances": [ranked["distances"]],
        "relevance_scores": [ranked["relevance_scores"]],
    }
