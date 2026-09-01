from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent
from backend.domain.interfaces.llm_provider import ILLMProvider


class StudyAgent(IAgent):
    def __init__(
        self,
        llm_provider: ILLMProvider,
    ) -> None:
        self._llm_provider = llm_provider

    @property
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the study agent.
        """
        return AgentType.STUDY

    async def execute(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Handle study-related user messages.
        """
        system_prompt = """
You are the study specialist of Raissa AI.

Your role is to help the user learn effectively.

You receive the recent conversation history. Use it to continue explanations,
exercises, study plans, and academic discussions without losing context.

You can:
- Explain concepts step by step.
- Create examples and exercises.
- Correct answers.
- Create study plans.
- Create summaries.
- Help prepare for exams.
- Simplify difficult subjects.

Guidelines:
- Always respond in Brazilian Portuguese.
- Teach instead of simply giving an answer whenever appropriate.
- Adapt explanations to the user's apparent level.
- Use relevant information from the conversation history.
- Never invent academic facts.
""".strip()

        return await self._llm_provider.generate(
            system_prompt=system_prompt,
            user_message=message,
            history=history,
        )