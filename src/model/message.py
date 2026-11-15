from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel

from beanie import Document
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class SourceReference(BaseModel):
    page_number: int
    chunk_id: str
    text: Optional[str] = None


class Message(Document):
    conversation_id: PydanticObjectId

    role: MessageRole
    content: str

    sources: list[SourceReference] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"
        indexes = [
            IndexModel([("conversation_id", ASCENDING), ("created_at", ASCENDING)])
        ]
