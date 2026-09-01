from abc import ABC, abstractmethod

from backend.application.dto.conversation import (
    ConversationHistory,
    ConversationSummary,
)


class IConversationReader(ABC):
    @abstractmethod
    async def list_conversations(
        self,
        limit: int = 50,
    ) -> list[ConversationSummary]:
        """
        Return the most recently updated conversations.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_conversation(
        self,
        conversation_id: str,
    ) -> ConversationHistory:
        """
        Return the complete history of a conversation.
        """
        raise NotImplementedError