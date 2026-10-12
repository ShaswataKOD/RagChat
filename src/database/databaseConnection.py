from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from src.config import config


@asynccontextmanager
async def database_lifespan(app: FastAPI):
    await startup_db_client(app)

    yield

    await shutdown_db_client(app)


async def startup_db_client(app: FastAPI):
    app.state.mongodb_client = AsyncMongoClient(config.config.database_url)

    await app.state.mongodb_client.admin.command("ping")

    print(f"MongoDB is connected at {config.config.database_url}")


async def shutdown_db_client(app: FastAPI):
    await app.state.mongodb_client.close()

    print("Database connection is shut down")
