# import httpx

# CHROMA_URL = "http://localhost:8000"

# TENANT = "default_tenant"
# DATABASE = "default_database"

# COLLECTION_NAME = "document_chunks"
# COLLECTION_ID = None

# BASE_PATH = f"/api/v2/tenants/{TENANT}/databases/{DATABASE}"


# def chroma_request(method: str, endpoint: str, payload=None):
#     url = f"{CHROMA_URL}{endpoint}"

#     response = httpx.request(method=method, url=url, json=payload, timeout=30)

#     if response.is_error:
#         print("ChromaDB Error:", response.status_code)
#         print("Response:", response.text)

#     response.raise_for_status()

#     if response.content:
#         return response.json()

#     return None


# def get_or_create_collection():
#     global COLLECTION_ID

#     # Reuse the ID if we already initialized the collection
#     if COLLECTION_ID is not None:
#         return COLLECTION_ID

#     collection_endpoint = f"{BASE_PATH}/collections/{COLLECTION_NAME}"

#     # First, check whether the collection already exists
#     response = httpx.get(f"{CHROMA_URL}{collection_endpoint}", timeout=30)

#     if response.status_code == 200:
#         collection = response.json()
#         print("Existing collection found:", COLLECTION_NAME)

#     elif response.status_code == 404:
#         # Collection doesn't exist, so create it
#         print("Collection not found. Creating a new collection...")

#         collection = chroma_request(
#             "POST",
#             f"{BASE_PATH}/collections",
#             {"name": COLLECTION_NAME, "metadata": {"hnsw:space": "cosine"}},
#         )

#         print("New collection created:", COLLECTION_NAME)

#     else:
#         response.raise_for_status()

#     COLLECTION_ID = collection["id"]

#     print("Collection ID:", COLLECTION_ID)

#     return COLLECTION_ID


# def get_collection_path():
#     collection_id = get_or_create_collection()

#     return f"{BASE_PATH}/collections/{collection_id}"


# def get_collection_count() -> int:
#     return chroma_request("GET", f"{get_collection_path()}/count")


# def upsert_chunks(
#     ids: list[str],
#     documents: list[str],
#     embeddings: list[list[float]],
#     metadatas: list[dict],
# ):
#     payload = {
#         "ids": ids,
#         "documents": documents,
#         "embeddings": embeddings,
#         "metadatas": metadatas,
#     }

#     return chroma_request("POST", f"{get_collection_path()}/upsert", payload)


# def query_chunks(query_embedding: list[float], n_results: int = 3):
#     payload = {
#         "query_embeddings": [query_embedding],
#         "n_results": n_results,
#         "include": ["documents", "metadatas", "distances"],
#     }

#     return chroma_request("POST", f"{get_collection_path()}/query", payload)


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
    n_results: int = 3,
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
