from pydantic import BaseModel, Field

from backend.domain.enums.agent_type import AgentType


class ChatRequest(BaseModel):
    conversation_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Conversation identifier.",
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=10_000,
        description="User message sent to Raissa AI.",
    )


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    agent: AgentType