from typing import Any

from backend.application.dto.chat import ChatInput
from backend.application.dto.document import (
    GenerateDocumentInput,
)
from backend.core.container import (
    build_generate_document_use_case,
    build_send_message_use_case,
    build_summarize_conversation_use_case,
)
from backend.domain.enums.document_format import (
    DocumentFormat,
)
from backend.infrastructure.database.postgres_conversation_reader import (
    PostgresConversationReader,
)
from frontend.services.async_runner import (
    run_async,
)


def send_message(
    message: str,
    conversation_id: str,
) -> dict[str, Any]:
    """
    Process a message directly through the application use case.
    """
    use_case = build_send_message_use_case()

    result = run_async(
        use_case.execute(
            ChatInput(
                conversation_id=conversation_id,
                message=message,
            )
        )
    )

    return {
        "conversation_id": result.conversation_id,
        "message": result.message,
        "agent": result.agent.value,
    }


def list_conversations() -> list[dict[str, Any]]:
    """
    Return the most recent conversations directly from PostgreSQL.
    """
    reader = PostgresConversationReader()

    conversations = run_async(
        reader.list_conversations()
    )

    return [
        {
            "conversation_id": conversation.conversation_id,
            "title": conversation.title,
            "updated_at": conversation.updated_at,
        }
        for conversation in conversations
    ]


def get_conversation(
    conversation_id: str,
) -> dict[str, Any]:
    """
    Return the complete history of a conversation.
    """
    reader = PostgresConversationReader()

    conversation = run_async(
        reader.get_conversation(
            conversation_id
        )
    )

    return {
        "conversation_id": conversation.conversation_id,
        "messages": [
            {
                "role": message.role.value,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in conversation.messages
        ],
    }


def prepare_conversation_material(
    conversation_id: str,
) -> dict[str, Any]:
    """
    Generate one summary and reuse it for PDF and DOCX documents.
    """
    summary_use_case = (
        build_summarize_conversation_use_case()
    )

    document_use_case = (
        build_generate_document_use_case()
    )

    summary = run_async(
        summary_use_case.execute(
            conversation_id
        )
    )

    pdf = document_use_case.execute(
        GenerateDocumentInput(
            title=summary.title,
            content=summary.summary,
            document_format=DocumentFormat.PDF,
        )
    )

    docx = document_use_case.execute(
        GenerateDocumentInput(
            title=summary.title,
            content=summary.summary,
            document_format=DocumentFormat.DOCX,
        )
    )

    return {
        "summary": {
            "conversation_id": summary.conversation_id,
            "title": summary.title,
            "summary": summary.summary,
        },
        "pdf": {
            "content": pdf.content,
            "filename": pdf.filename,
            "media_type": pdf.media_type,
        },
        "docx": {
            "content": docx.content,
            "filename": docx.filename,
            "media_type": docx.media_type,
        },
    }