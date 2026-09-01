from abc import ABC, abstractmethod

from backend.domain.entities.chat_message import ChatMessage


class IConversationMemory(ABC):
    @abstractmethod
    async def add_message(
        self,
        message: ChatMessage,
    ) -> None:
        """
        Store a message in the conversation history.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_history(
        self,
        conversation_id: str,
        limit: int = 20,
    ) -> list[ChatMessage]:
        """
        Return the most recent messages for a conversation.
        """
        raise NotImplementedError

    @abstractmethod
    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all stored messages from a conversation.
        """
        raise NotImplementedError