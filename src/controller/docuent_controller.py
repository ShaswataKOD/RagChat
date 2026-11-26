from beanie import PydanticObjectId
from fastapi import HTTPException, UploadFile

from src.schema.document_schema import DocumentResponse
from src.service.documentation_service import DocumentService


class DocumentController:
    @staticmethod
    async def upload_document(
        file: UploadFile, user_id: PydanticObjectId
    ) -> DocumentResponse:

        try:
            document = await DocumentService.upload_document(file=file, user_id=user_id)

            return DocumentResponse(
                id=str(document.id),
                filename=document.filename,
                status=document.status.value,
                created_at=document.created_at,
            )

        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))
