from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent_router import IAgentRouter


class FakeAgentRouter(IAgentRouter):
    async def route(self, message: str) -> AgentType:
        """
        Route every message to the general agent.
        """
        return AgentType.GENERAL