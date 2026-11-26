from src.model.conversation import Conversation
from src.model.message import Message
from src.model.message import MessageRole
from src.model.document import UploadedDocument, DocumentStatus
from beanie import PydanticObjectId
from datetime import datetime, timezone
from starlette.concurrency import run_in_threadpool
from src.rag.query import ask_question
from src.model.User import User
from src.model.message import Message


class chatService:
    @staticmethod
    async def chat_with_pdf(document_id, user_id, question):

        requested_document = await UploadedDocument.find_one(
            UploadedDocument.id == document_id, UploadedDocument.user_id == user_id
        )

        if requested_document is None:
            raise ValueError("File not found")

        if requested_document.status != DocumentStatus.COMPLETED:
            raise ValueError("File not ready for querying")

        # try to find if there is a previous conversation or chat existis
        conversation = await Conversation.find(
            Conversation.document_id == document_id, Conversation.user_id == user_id
        ).first_or_none()

        if conversation is None:
            conversation = Conversation(user_id=user_id, document_id=document_id)

            await conversation.insert()

        if conversation.id is None:
            raise ValueError("Conversation ID was not generated")

        user_message = Message(
            conversation_id=conversation.id, role=MessageRole.USER, content=question
        )

        await user_message.save()

        # we will be generating answer

        answer = await run_in_threadpool(
            ask_question, question, str(user_id), str(document_id)
        )

        llm_answer = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=answer,
        )

        await llm_answer.insert()

        conversation.updated_at = datetime.now(timezone.utc)

        await conversation.save()

        return {
            "conversation_id": str(conversation.id),
            "document_id": str(document_id),
            "answer": answer,
        }

    @staticmethod
    async def get_document_messages(document_id, user_id):
        if not user_id:
            raise ValueError("user id is invalid ")
        if not document_id:
            raise ValueError("doc id is invalid")

        existing_user = await User.get(user_id)

        if existing_user:
            existing_document = await UploadedDocument.find_one(
                UploadedDocument.id == document_id,
                UploadedDocument.user_id == user_id,
                UploadedDocument.status == DocumentStatus.COMPLETED,
            )

            if not existing_document:
                raise ValueError("No matching document has been found")

            existing_conversation = await Conversation.find_one(
                Conversation.document_id == document_id, Conversation.user_id == user_id
            )

            if not existing_conversation:
                raise ValueError("No conversation is recorded or created")

            chats_from_documents = (
                await Message.find(Message.conversation_id == existing_conversation.id)
                .sort("created_at", "desc")
                .to_list()
            )

            return {
                "conversation_id": str(existing_conversation.id),
                "document_id": str(document_id),
                "messages": [
                    {"role": message.role, "content": message.content}
                    for message in chats_from_documents
                ],
            }
