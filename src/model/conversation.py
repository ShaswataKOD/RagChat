from datetime import datetime, timezone

from beanie import Document
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


class Conversation(Document):
    user_id: PydanticObjectId
    document_id: PydanticObjectId

    title: str = "New Conversation"

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "conversations"
        indexes = [
            IndexModel([("document_id", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING)]),
        ]
