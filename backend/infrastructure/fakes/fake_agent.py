from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent


class FakeAgent(IAgent):
    def __init__(self, agent_type: AgentType) -> None:
        self._agent_type = agent_type

    @property
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the fake agent.
        """
        return self._agent_type

    async def execute(self, message: str) -> str:
        """
        Return a deterministic fake response for testing purposes.
        """
        return (
            f"Message received by {self._agent_type.value} agent: "
            f"{message}"
        )