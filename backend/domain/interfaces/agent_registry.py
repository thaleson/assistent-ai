from abc import ABC, abstractmethod

from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent


class IAgentRegistry(ABC):
    @abstractmethod
    def get(self, agent_type: AgentType) -> IAgent:
        """
        Return the agent registered for the given agent type.
        """
        raise NotImplementedError