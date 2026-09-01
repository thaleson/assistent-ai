from collections.abc import Iterable

from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent
from backend.domain.interfaces.agent_registry import IAgentRegistry


class AgentRegistry(IAgentRegistry):
    def __init__(self, agents: Iterable[IAgent]) -> None:
        self._agents = {
            agent.agent_type: agent
            for agent in agents
        }

    def get(self, agent_type: AgentType) -> IAgent:
        """
        Return the agent registered for the requested type.
        """
        agent = self._agents.get(agent_type)

        if agent is None:
            raise ValueError(
                f"No agent registered for type: {agent_type.value}"
            )

        return agent