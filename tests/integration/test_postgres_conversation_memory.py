from uuid import uuid4

import pytest

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.message_role import MessageRole
from backend.infrastructure.database.postgres_conversation_memory import (
    PostgresConversationMemory,
)


@pytest.mark.asyncio
async def test_postgres_memory_persists_messages() -> None:
    memory = PostgresConversationMemory()

    conversation_id = (
        f"test-{uuid4()}"
    )

    try:
        await memory.add_message(
            ChatMessage.create(
                conversation_id=conversation_id,
                role=MessageRole.USER,
                content="Persistent test message",
            )
        )

        history = await memory.get_history(
            conversation_id
        )

        assert len(history) == 1

        assert history[0].content == (
            "Persistent test message"
        )

        assert history[0].role == (
            MessageRole.USER
        )

    finally:
        await memory.clear(
            conversation_id
        )