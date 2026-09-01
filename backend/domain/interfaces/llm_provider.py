from abc import ABC, abstractmethod

from backend.domain.entities.chat_message import ChatMessage


class ILLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Generate a response using the conversation history.
        """
        raise NotImplementedError