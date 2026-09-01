from dataclasses import dataclass

from backend.domain.enums.agent_type import AgentType


@dataclass(frozen=True, slots=True)
class ChatInput:
    conversation_id: str
    message: str


@dataclass(frozen=True, slots=True)
class ChatOutput:
    conversation_id: str
    message: str
    agent: AgentType