import pytest

from backend.application.dto.chat import ChatInput
from backend.application.use_cases.send_message import SendMessageUseCase
from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.message_role import MessageRole
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent
from backend.domain.interfaces.agent_registry import IAgentRegistry
from backend.domain.interfaces.agent_router import IAgentRouter
from backend.infrastructure.memory.in_memory_conversation_memory import (
    InMemoryConversationMemory,
)


class FakerRouter(IAgentRouter):
    async def route(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> AgentType:
        """
        Route every message to the general agent.
        """
        return AgentType.GENERAL


class FakerRouter(IAgentRouter):
    async def route(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> AgentType:
        """
        Route every message to the general agent.
        """
        return AgentType.GENERAL


class FakerAgent(IAgent):
    @property
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the test agent.
        """
        return AgentType.GENERAL

    async def execute(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Return a deterministic response for testing.
        """
        return f"Response to: {message}"


class FakerRegistry(IAgentRegistry):
    def __init__(
        self,
        agent: IAgent,
    ) -> None:
        self._agent = agent
        self._registry: dict[AgentType, IAgent] = {agent.agent_type: agent}

    def register(
        self,
        agent: IAgent,
    ) -> None:
        """
        Register an agent by its type so the registry can be queried later.
        """
        self._registry[agent.agent_type] = agent

    def get(
        self,
        agent_type: AgentType,
    ) -> IAgent:
        """
        Return the configured test agent.
        """
        if agent_type not in self._registry:
            raise KeyError(f"No agent registered for {agent_type}")
        return self._registry[agent_type]

    def get_all(self) -> dict[AgentType, IAgent]:
        """
        Return a copy of the current registry contents.
        """
        return dict(self._registry)


@pytest.mark.asyncio
async def test_send_message_use_case_persists_conversation() -> None:
    memory = InMemoryConversationMemory()

    agent = FakerAgent()

    use_case = SendMessageUseCase(
        agent_router=FakerRouter(),
        agent_registry=FakerRegistry(
            agent=agent,
        ),
        conversation_memory=memory,
    )

    result = await use_case.execute(
        ChatInput(
            conversation_id="conversation-001",
            message="Hello Raissa AI",
        )
    )

    history = await memory.get_history(
        "conversation-001"
    )

    assert result.conversation_id == "conversation-001"

    assert result.agent == AgentType.GENERAL

    assert result.message == (
        "Response to: Hello Raissa AI"
    )

    assert len(history) == 2

    assert history[0].content == "Hello Raissa AI"

    assert history[1].content == (
        "Response to: Hello Raissa AI"
    )


@pytest.mark.asyncio
async def test_send_message_use_case_passes_history_to_agent() -> None:
    received_history: list[ChatMessage] = []

    class HistoryAgent(IAgent):
        @property
        def agent_type(self) -> AgentType:
            """
            Return the type handled by the test agent.
            """
            return AgentType.GENERAL

        async def execute(
            self,
            message: str,
            history: list[ChatMessage],
        ) -> str:
            """
            Store the received history for assertions.
            """
            received_history.extend(
                history
            )

            return "Context received"

    memory = InMemoryConversationMemory()

    await memory.add_message(
        ChatMessage.create(
            conversation_id="context-test",
            role=MessageRole.USER,
            content="My name is Raissa",
        )
    )

    agent = HistoryAgent()

    use_case = SendMessageUseCase(
        agent_router=FakerRouter(),
        agent_registry=FakerRegistry(
            agent=agent,
        ),
        conversation_memory=memory,
    )

    await use_case.execute(
        ChatInput(
            conversation_id="context-test",
            message="What is my name?",
        )
    )

    assert len(received_history) == 1

    assert received_history[0].content == (
        "My name is Raissa"
    )