import chromadb

from typing import Any


# ChromaDB server configuration
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000

TENANT = "default_tenant"
DATABASE = "default_database"

COLLECTION_NAME = "document_chunks"


# Connect to the existing ChromaDB server running in Docker
client = chromadb.HttpClient(
    host=CHROMA_HOST,
    port=CHROMA_PORT,
    tenant=TENANT,
    database=DATABASE,
)


def get_or_create_collection():
    """
    Retrieve the existing collection or create it if unavailable.
    """

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    return collection


def get_collection_count() -> int:
    """
    Return the total number of stored chunks.
    """

    collection = get_or_create_collection()

    return collection.count()


def upsert_chunks(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict[str, Any]],
):
    """
    Insert or update document chunks in ChromaDB.
    """

    if not (len(ids) == len(documents) == len(embeddings) == len(metadatas)):
        raise ValueError("All input lists must have equal lengths")

    collection = get_or_create_collection()

    return collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_chunks(
    query_embedding: list[float],
    n_results: int = 15,
    where: dict[str, Any] | None = None,
):
    """
    Retrieve similar chunks, optionally filtering by metadata.
    """

    collection = get_or_create_collection()

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": n_results,
        "include": ["documents", "metadatas", "distances"],
    }

    if where is not None:
        query_args["where"] = where

    return collection.query(**query_args)


def delete_collection():
    """Delete the entire document_chunks collection."""

    existing_collections = client.list_collections()

    if any(c.name == COLLECTION_NAME for c in existing_collections):
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' deleted successfully.")
    else:
        print(f"Collection '{COLLECTION_NAME}' does not exist.")


def get_collection_details(user_id: str, document_id: str):

    collection = get_or_create_collection()

    results = collection.get(
        where={"$and": [{"user_id": user_id}, {"document_id": document_id}]},
        # include=["documents", "metadatas"],
    )

    print("Number of records:", len(results["ids"]))
    print("IDs:", results["ids"])
    print("Metadata:", results["metadatas"])

    return results
