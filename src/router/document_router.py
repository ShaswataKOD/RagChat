from fastapi import APIRouter, Depends, File, UploadFile, status

from src.auth.auth import get_current_user
from src.model.User import User
from src.controller.docuent_controller import DocumentController
from src.schema.document_schema import DocumentResponse

document_router = APIRouter(prefix="/documents", tags=["Documents"])


@document_router.post(
    "/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
async def upload_document(
    file: UploadFile = File(...), current_user: User = Depends(get_current_user)
):
    return await DocumentController.upload_document(file=file, user_id=current_user.id)
