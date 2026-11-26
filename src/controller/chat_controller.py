from src.service.chat_service import chatService


class ChatController:
    @staticmethod
    async def chat_with_document(document_id, user_id, question):
        return await chatService.chat_with_pdf(
            document_id=document_id, user_id=user_id, question=question
        )

    @staticmethod
    async def get_document_messages(document_id, user_id):
        return await chatService.get_document_messages(
            document_id=document_id, user_id=user_id
        )
