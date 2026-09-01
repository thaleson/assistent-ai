from fastapi import APIRouter, Depends

from backend.application.dto.chat import ChatInput
from backend.application.use_cases.send_message import SendMessageUseCase
from backend.core.container import build_send_message_use_case
from backend.presentation.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send a message to Raissa AI",
)
async def send_message(
    request: ChatRequest,
    use_case: SendMessageUseCase = Depends(
        build_send_message_use_case
    ),
) -> ChatResponse:
    """
    Receive a user message and delegate processing to the application layer.
    """
    chat_input = ChatInput(
        conversation_id=request.conversation_id,
        message=request.message,
    )

    result = await use_case.execute(
        chat_input
    )

    return ChatResponse(
        conversation_id=result.conversation_id,
        message=result.message,
        agent=result.agent,
    )