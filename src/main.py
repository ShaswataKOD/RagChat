from fastapi import FastAPI
from src.router.authRoute import auth_router
from src.database.databaseConnection import database_lifespan

app = FastAPI(
    title="RAG Chat API",
    description="""
    ## Document-based RAG Chat Application

    An API for uploading PDF documents, managing conversations,
    and asking questions using Retrieval-Augmented Generation.

    ### Main Features
    - User registration and authentication
    - PDF document upload and management
    - Document-specific conversations
    - Context-aware question answering
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=database_lifespan,
)

app.include_router(auth_router)


@app.get("/", tags=["General"])
async def root():
    return {"message": "RAG Chat API is running"}
