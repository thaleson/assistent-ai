from abc import ABC, abstractmethod

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType


class IAgentRouter(ABC):
    @abstractmethod
    async def route(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> AgentType:
        """
        Determine which agent type should handle the user message.
        """
        raise NotImplementedError