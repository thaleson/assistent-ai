from dataclasses import dataclass
from datetime import datetime

from backend.domain.entities.chat_message import ChatMessage


@dataclass(frozen=True, slots=True)
class ConversationSummary:
    conversation_id: str
    title: str
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class ConversationHistory:
    conversation_id: str
    messages: list[ChatMessage]