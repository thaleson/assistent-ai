from sqlalchemy import delete, select

from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.message_role import MessageRole
from backend.domain.interfaces.conversation_memory import IConversationMemory
from backend.infrastructure.database.models.chat_message_model import (
    ChatMessageModel,
)
from backend.infrastructure.database.session import AsyncSessionFactory


class PostgresConversationMemory(IConversationMemory):
    async def add_message(
        self,
        message: ChatMessage,
    ) -> None:
        """
        Persist a conversation message in PostgreSQL.
        """
        async with AsyncSessionFactory() as session:
            model = ChatMessageModel(
                conversation_id=message.conversation_id,
                role=message.role.value,
                content=message.content,
                created_at=message.created_at,
            )

            session.add(model)

            await session.commit()

    async def get_history(
        self,
        conversation_id: str,
        limit: int = 20,
    ) -> list[ChatMessage]:
        """
        Return the most recent messages for a conversation.
        """
        if limit <= 0:
            return []

        async with AsyncSessionFactory() as session:
            statement = (
                select(ChatMessageModel)
                .where(
                    ChatMessageModel.conversation_id
                    == conversation_id
                )
                .order_by(
                    ChatMessageModel.created_at.desc()
                )
                .limit(limit)
            )

            result = await session.execute(statement)

            models = list(
                result.scalars().all()
            )

        models.reverse()

        return [
            ChatMessage(
                conversation_id=model.conversation_id,
                role=MessageRole(model.role),
                content=model.content,
                created_at=model.created_at,
            )
            for model in models
        ]

    async def clear(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all messages associated with a conversation.
        """
        async with AsyncSessionFactory() as session:
            statement = delete(
                ChatMessageModel
            ).where(
                ChatMessageModel.conversation_id
                == conversation_id
            )

            await session.execute(statement)
            await session.commit()