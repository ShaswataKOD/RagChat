from datetime import datetime, timezone
from enum import Enum

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel
from beanie import Document, PydanticObjectId


class DocumentStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    UPLOADED = "uploaded"


class UploadedDocument(Document):
    user_id: PydanticObjectId

    filename: str
    file_path: str

    status: DocumentStatus = DocumentStatus.PROCESSING

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "documents"
        indexes = [IndexModel([("user_id", ASCENDING)])]
