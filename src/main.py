from fastapi import FastAPI
from src.router.chat_router import chat_router
from src.router.document_router import document_router
from src.router.authRoute import auth_router
from src.database.databaseConnection import database_lifespan
from src.middleware.performance import measure_response_time
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

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
app.include_router(document_router)
app.include_router(chat_router)


# register the middleware
app.middleware(middleware_type="http")(measure_response_time)


@app.get("/", tags=["General"])
async def root():
    return {"message": "RAG Chat API is running"}
