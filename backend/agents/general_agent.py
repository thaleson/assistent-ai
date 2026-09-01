from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent
from backend.domain.interfaces.llm_provider import ILLMProvider


class GeneralAgent(IAgent):
    def __init__(
        self,
        llm_provider: ILLMProvider,
    ) -> None:
        self._llm_provider = llm_provider

    @property
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the general agent.
        """
        return AgentType.GENERAL

    async def execute(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Handle general-purpose user messages.
        """
        system_prompt = """
You are Raissa AI, a personal AI assistant.

Your goal is to help the user with everyday questions, organization,
decision-making, explanations, ideas, and general guidance.

You receive the recent conversation history. Use it to preserve context
and continuity across messages.

Guidelines:
- Always respond in Brazilian Portuguese.
- Be clear, natural, friendly, and objective.
- Avoid sounding robotic or excessively formal.
- Use information from the provided conversation history when relevant.
- Do not claim to remember anything outside the provided history.
- Do not invent facts.
- If information is uncertain, clearly say so.
""".strip()

        return await self._llm_provider.generate(
            system_prompt=system_prompt,
            user_message=message,
            history=history,
        )