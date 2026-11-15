from fastapi import FastAPI

from src.database.databaseConnection import database_lifespan

app = FastAPI(
    title="RAG Chat API",
    description="Document-based RAG application",
    version="1.0.0",
    lifespan=database_lifespan,
)


@app.get("/")
async def root():
    return {"message": "RAG Chat API is running"}
