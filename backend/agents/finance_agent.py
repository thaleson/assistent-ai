from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent import IAgent
from backend.domain.interfaces.llm_provider import ILLMProvider


class FinanceAgent(IAgent):
    def __init__(
        self,
        llm_provider: ILLMProvider,
    ) -> None:
        self._llm_provider = llm_provider

    @property
    def agent_type(self) -> AgentType:
        """
        Return the type handled by the finance agent.
        """
        return AgentType.FINANCE

    async def execute(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> str:
        """
        Handle finance-related user messages.
        """
        system_prompt = """
You are the personal finance specialist of Raissa AI.

Your role is to help the user understand and organize personal finances.

You receive the recent conversation history. Use it to preserve financial
context such as income, expenses, goals, debts, and prior calculations.

You can help with:
- Monthly budgeting.
- Expense organization.
- Financial goals.
- Emergency reserves.
- Debt planning.
- Compound interest calculations.
- Investment education.
- Saving strategies.
- Income planning.

Guidelines:
- Always respond in Brazilian Portuguese.
- Explain calculations clearly.
- Use relevant financial information from the conversation history.
- Distinguish facts from assumptions.
- Never invent current financial rates or market prices.
- Avoid promising profit or guaranteed returns.
""".strip()

        return await self._llm_provider.generate(
            system_prompt=system_prompt,
            user_message=message,
            history=history,
        )