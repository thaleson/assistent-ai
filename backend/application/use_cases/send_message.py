from backend.application.dto.chat import ChatInput, ChatOutput
from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.message_role import MessageRole
from backend.domain.interfaces.agent_registry import IAgentRegistry
from backend.domain.interfaces.agent_router import IAgentRouter
from backend.domain.interfaces.conversation_memory import IConversationMemory


class SendMessageUseCase:
    def __init__(
        self,
        agent_router: IAgentRouter,
        agent_registry: IAgentRegistry,
        conversation_memory: IConversationMemory,
    ) -> None:
        self._agent_router = agent_router
        self._agent_registry = agent_registry
        self._conversation_memory = conversation_memory

    async def execute(
        self,
        chat_input: ChatInput,
    ) -> ChatOutput:
        """
        Process a chat message using the recent conversation history.
        """
        history = await self._conversation_memory.get_history(
            conversation_id=chat_input.conversation_id,
            limit=20,
        )

        agent_type = await self._agent_router.route(
            message=chat_input.message,
            history=history,
        )

        agent = self._agent_registry.get(
            agent_type
        )

        response = await agent.execute(
            message=chat_input.message,
            history=history,
        )

        await self._conversation_memory.add_message(
            ChatMessage.create(
                conversation_id=chat_input.conversation_id,
                role=MessageRole.USER,
                content=chat_input.message,
            )
        )

        await self._conversation_memory.add_message(
            ChatMessage.create(
                conversation_id=chat_input.conversation_id,
                role=MessageRole.ASSISTANT,
                content=response,
            )
        )

        return ChatOutput(
            conversation_id=chat_input.conversation_id,
            message=response,
            agent=agent_type,
        )