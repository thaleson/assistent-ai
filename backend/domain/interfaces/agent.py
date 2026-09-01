from abc import ABC, abstractmethod

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType


class IAgent(ABC):
    @property
    @abstractmethod
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the agent.
        """
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Process a user message using the conversation history.
        """
        raise NotImplementedError