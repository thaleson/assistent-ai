from backend.agents.agent_registry import AgentRegistry
from backend.agents.finance_agent import FinanceAgent
from backend.agents.general_agent import GeneralAgent
from backend.agents.llm_agent_router import LLMAgentRouter
from backend.agents.study_agent import StudyAgent
from backend.application.use_cases.send_message import SendMessageUseCase
from backend.core.config import get_settings
from backend.infrastructure.database.postgres_conversation_memory import (
    PostgresConversationMemory,
)
from backend.infrastructure.llm.groq_llm_provider import GroqLLMProvider

from backend.application.use_cases.summarize_conversation import (
    SummarizeConversationUseCase,
)
from backend.infrastructure.database.postgres_conversation_reader import (
    PostgresConversationReader,
)

from backend.application.use_cases.generate_document import (
    GenerateDocumentUseCase,
)
from backend.infrastructure.documents.docx_document_generator import (
    DocxDocumentGenerator,
)
from backend.infrastructure.documents.pdf_document_generator import (
    PdfDocumentGenerator,
)
def build_send_message_use_case() -> SendMessageUseCase:
    """
    Build and wire the dependencies required by the send message use case.
    """
    settings = get_settings()

    llm_provider = GroqLLMProvider(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )

    general_agent = GeneralAgent(
        llm_provider=llm_provider,
    )

    study_agent = StudyAgent(
        llm_provider=llm_provider,
    )

    finance_agent = FinanceAgent(
        llm_provider=llm_provider,
    )

    agent_router = LLMAgentRouter(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )

    agent_registry = AgentRegistry(
        agents=[
            general_agent,
            study_agent,
            finance_agent,
        ]
    )

    conversation_memory = PostgresConversationMemory()

    return SendMessageUseCase(
        agent_router=agent_router,
        agent_registry=agent_registry,
        conversation_memory=conversation_memory,
    )


def build_summarize_conversation_use_case(
) -> SummarizeConversationUseCase:
    """
    Build the conversation summarization use case.
    """
    settings = get_settings()

    llm_provider = GroqLLMProvider(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
    )

    conversation_reader = (
        PostgresConversationReader()
    )

    return SummarizeConversationUseCase(
        conversation_reader=conversation_reader,
        llm_provider=llm_provider,
    )


def build_generate_document_use_case() -> GenerateDocumentUseCase:
    """
    Build the document generation use case.
    """
    return GenerateDocumentUseCase(
        generators=[
            PdfDocumentGenerator(),
            DocxDocumentGenerator(),
        ]
    )