from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.agent_type import AgentType
from backend.domain.interfaces.agent_router import IAgentRouter


class KeywordAgentRouter(IAgentRouter):
    STUDY_KEYWORDS = {
        "curso",
        "cursos",
        "estudante",
        "estudar",
        "estudo",
        "prova",
        "faculdade",
        "escola",
        "matéria",
        "materia",
        "matemática",
        "matematica",
        "aprender",
        "ensinar",
        "explique",
        "explicar",
        "resumo",
        "aula",
        "regra de três",
        "regra de tres",
        "porcentagem",
    }

    FINANCE_KEYWORDS = {
        "dinheiro",
        "finança",
        "financa",
        "finanças",
        "financas",
        "salário",
        "salario",
        "gasto",
        "gastos",
        "dívida",
        "divida",
        "investimento",
        "investir",
        "poupar",
        "economizar",
        "renda",
        "juros",
        "orçamento",
        "orcamento",
    }

    async def route(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> AgentType:
        """
        Route the user message using a simple keyword-based strategy.
        """
        normalized_message = message.lower().strip()

        if any(
            keyword in normalized_message
            for keyword in self.STUDY_KEYWORDS
        ):
            return AgentType.STUDY

        if any(
            keyword in normalized_message
            for keyword in self.FINANCE_KEYWORDS
        ):
            return AgentType.FINANCE

        return AgentType.GENERAL