from pydantic import BaseModel, Field, field_validator


class requestChatSchema(BaseModel):
    question: str = Field(min_length=1, max_length=200)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Question can't be empty")

        return value


class responseChatSchema(BaseModel):
    conversation_id: str
    document_id: str
    answer: str
