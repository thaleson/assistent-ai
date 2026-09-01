import pytest

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.message_role import MessageRole
from backend.infrastructure.memory.in_memory_conversation_memory import (
    InMemoryConversationMemory,
)


@pytest.mark.asyncio
async def test_memory_stores_and_returns_messages() -> None:
    memory = InMemoryConversationMemory()

    message = ChatMessage.create(
        conversation_id="conversation-001",
        role=MessageRole.USER,
        content="Hello",
    )

    await memory.add_message(
        message
    )

    history = await memory.get_history(
        "conversation-001"
    )

    assert len(history) == 1
    assert history[0].content == "Hello"
    assert history[0].role == MessageRole.USER


@pytest.mark.asyncio
async def test_memory_isolates_conversations() -> None:
    memory = InMemoryConversationMemory()

    await memory.add_message(
        ChatMessage.create(
            conversation_id="conversation-a",
            role=MessageRole.USER,
            content="Message A",
        )
    )

    await memory.add_message(
        ChatMessage.create(
            conversation_id="conversation-b",
            role=MessageRole.USER,
            content="Message B",
        )
    )

    history_a = await memory.get_history(
        "conversation-a"
    )

    history_b = await memory.get_history(
        "conversation-b"
    )

    assert len(history_a) == 1
    assert len(history_b) == 1

    assert history_a[0].content == "Message A"
    assert history_b[0].content == "Message B"


@pytest.mark.asyncio
async def test_memory_respects_history_limit() -> None:
    memory = InMemoryConversationMemory()

    for index in range(5):
        await memory.add_message(
            ChatMessage.create(
                conversation_id="conversation-limit",
                role=MessageRole.USER,
                content=f"Message {index}",
            )
        )

    history = await memory.get_history(
        conversation_id="conversation-limit",
        limit=2,
    )

    assert len(history) == 2

    assert history[0].content == "Message 3"
    assert history[1].content == "Message 4"


@pytest.mark.asyncio
async def test_memory_can_clear_conversation() -> None:
    memory = InMemoryConversationMemory()

    await memory.add_message(
        ChatMessage.create(
            conversation_id="conversation-clear",
            role=MessageRole.USER,
            content="Temporary message",
        )
    )

    await memory.clear(
        "conversation-clear"
    )

    history = await memory.get_history(
        "conversation-clear"
    )

    assert history == []