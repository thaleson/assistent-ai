from fastapi import APIRouter, HTTPException

from backend.infrastructure.database.postgres_conversation_reader import (
    PostgresConversationReader,
)

from fastapi.responses import Response

from backend.application.dto.document import (
    GenerateDocumentInput,
)
from backend.core.container import (
    build_generate_document_use_case,
    build_summarize_conversation_use_case,
)
from backend.domain.enums.document_format import (
    DocumentFormat,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.get("")
async def list_conversations() -> list[dict]:
    """
    Return the most recent conversations.
    """
    reader = PostgresConversationReader()

    conversations = await reader.list_conversations()

    return [
        {
            "conversation_id": conversation.conversation_id,
            "title": conversation.title,
            "updated_at": conversation.updated_at,
        }
        for conversation in conversations
    ]


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
) -> dict:
    """
    Return the complete history for a conversation.
    """
    reader = PostgresConversationReader()

    conversation = await reader.get_conversation(
        conversation_id
    )

    if not conversation.messages:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
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


@router.post(
    "/{conversation_id}/summary"
)
async def summarize_conversation(
    conversation_id: str,
) -> dict:
    """
    Generate a structured summary of a conversation.
    """
    use_case = (
        build_summarize_conversation_use_case()
    )

    try:
        result = await use_case.execute(
            conversation_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return {
        "conversation_id": (
            result.conversation_id
        ),
        "title": result.title,
        "summary": result.summary,
    }


@router.get(
    "/{conversation_id}/summary/{document_format}"
)
async def download_conversation_summary(
    conversation_id: str,
    document_format: DocumentFormat,
) -> Response:
    """
    Generate and return a conversation summary document.
    """
    summarize_use_case = (
        build_summarize_conversation_use_case()
    )

    document_use_case = (
        build_generate_document_use_case()
    )

    try:
        summary = await summarize_use_case.execute(
            conversation_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    document = document_use_case.execute(
        GenerateDocumentInput(
            title=summary.title,
            content=summary.summary,
            document_format=document_format,
        )
    )

    return Response(
        content=document.content,
        media_type=document.media_type,
        headers={
            "Content-Disposition": (
                f'attachment; filename="{document.filename}"'
            )
        },
    )