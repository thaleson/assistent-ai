from dataclasses import dataclass
from datetime import datetime, timezone

from backend.domain.enums.message_role import MessageRole


@dataclass(frozen=True, slots=True)
class ChatMessage:
    conversation_id: str
    role: MessageRole
    content: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        conversation_id: str,
        role: MessageRole,
        content: str,
    ) -> "ChatMessage":
        """
        Create a chat message using the current UTC timestamp.
        """
        return cls(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
