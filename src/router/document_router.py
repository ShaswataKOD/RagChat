from fastapi import APIRouter, UploadFile, File, Depends

from src.dependencies.auth import get_current_user
from src.models.user import User

document_router = APIRouter(prefix="/documents", tags=["Documents"])


@document_router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), current_user: User = Depends(get_current_user)
):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "user_id": str(current_user.id),
    }
