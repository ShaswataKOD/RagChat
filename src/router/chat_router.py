from fastapi import APIRouter, Depends
from beanie import PydanticObjectId

from src.auth.auth import get_current_user
from src.model.User import User
from src.controller.chat_controller import ChatController
from src.schema.chat_schema import requestChatSchema, responseChatSchema

chat_router = APIRouter(prefix="/documents", tags=["Chat"])


@chat_router.post("/{document_id}/chat", response_model=responseChatSchema)
async def chat_with_document(
    document_id: PydanticObjectId,
    request: requestChatSchema,
    current_user: User = Depends(get_current_user),
):
    return await ChatController.chat_with_document(
        document_id=document_id, user_id=current_user.id, question=request.question
    )
