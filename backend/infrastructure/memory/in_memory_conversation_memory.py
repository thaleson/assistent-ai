from backend.domain.entities.chat_message import ChatMessage
from backend.domain.interfaces.conversation_memory import IConversationMemory


class InMemoryConversationMemory(IConversationMemory):
    def __init__(self) -> None:
        self._conversations: dict[str, list[ChatMessage]] = {}

    async def add_message(
        self,
        message: ChatMessage,
    ) -> None:
        """
        Store a message in memory for the associated conversation.
        """
        conversation = self._conversations.setdefault(
            message.conversation_id,
            [],
        )

        conversation.append(message)

    async def get_history(
        self,
        conversation_id: str,
        limit: int = 20,
    ) -> list[ChatMessage]:
        """
        Return the most recent messages stored for a conversation.
        """
        conversation = self._conversations.get(
            conversation_id,
            [],
        )

        if limit <= 0:
            return []

        return list(
            conversation[-limit:]
        )

    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all messages associated with a conversation.
        """
        self._conversations.pop(
            conversation_id,
            None,
        )