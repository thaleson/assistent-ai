import pytest

from backend.agents.agent_registry import AgentRegistry
from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent



class FakeAgent(IAgent):
    def __init__(
        self,
        agent_type: AgentType,
    ) -> None:
        self._agent_type = agent_type

    @property
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the test agent.
        """
        return self._agent_type

    async def execute(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Return a deterministic response for testing.
        """
        return message


def test_registry_returns_registered_agent() -> None:
    agent = FakeAgent(
        agent_type=AgentType.GENERAL
    )

    registry = AgentRegistry(
        agents=[agent]
    )

    result = registry.get(
        AgentType.GENERAL
    )

    assert result is agent


def test_registry_raises_error_for_missing_agent() -> None:
    registry = AgentRegistry(
        agents=[]
    )

    with pytest.raises(
        ValueError,
        match="No agent registered",
    ):
        registry.get(
            AgentType.FINANCE
        )