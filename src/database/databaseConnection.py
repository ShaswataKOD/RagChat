from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from src.model.User import User
from src.model.conversation import Conversation
from src.model.document import UploadedDocument
from src.model.message import Message
from src.config.config import config


@asynccontextmanager
async def database_lifespan(app: FastAPI):

    # 1. Create MongoDB client
    client = AsyncMongoClient(config.database_url)

    try:
        # 2. Verify database connectivity
        await client.admin.command("ping")

        # 3. Select database
        database = client[config.database_name]

        # 4. Initialize Beanie
        await init_beanie(
            database=database,
            document_models=[User, UploadedDocument, Conversation, Message],
        )

        # 5. Store client and database in application state
        app.state.mongodb_client = client
        app.state.database = database

        print("MongoDB connected successfully")
        print("Beanie initialized successfully")

        yield

    finally:
        # 6. Close connection during application shutdown
        await client.close()
        print("MongoDB connection closed")
