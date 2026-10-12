from fastapi import FastAPI
from src.database.databaseConnection import database_lifespan

app = FastAPI(lifespan=database_lifespan)

print("app is running")
