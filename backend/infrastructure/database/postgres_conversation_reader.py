from sqlalchemy import func, select

from backend.application.dto.conversation import (
    ConversationHistory,
    ConversationSummary,
)
from backend.domain.entities.chat_message import ChatMessage
from backend.domain.enums.message_role import MessageRole
from backend.domain.interfaces.conversation_reader import (
    IConversationReader,
)
from backend.infrastructure.database.models.chat_message_model import (
    ChatMessageModel,
)
from backend.infrastructure.database.session import (
    AsyncSessionFactory,
)


class PostgresConversationReader(IConversationReader):
    async def list_conversations(
        self,
        limit: int = 50,
    ) -> list[ConversationSummary]:
        """
        Return recently updated conversations stored in PostgreSQL.
        """
        async with AsyncSessionFactory() as session:
            statement = (
                select(
                    ChatMessageModel.conversation_id,
                    func.max(
                        ChatMessageModel.created_at
                    ).label("updated_at"),
                )
                .group_by(
                    ChatMessageModel.conversation_id
                )
                .order_by(
                    func.max(
                        ChatMessageModel.created_at
                    ).desc()
                )
                .limit(limit)
            )

            result = await session.execute(
                statement
            )

            rows = result.all()

            conversations: list[
                ConversationSummary
            ] = []

            for row in rows:
                title = await self._get_title(
                    session=session,
                    conversation_id=row.conversation_id,
                )

                conversations.append(
                    ConversationSummary(
                        conversation_id=row.conversation_id,
                        title=title,
                        updated_at=row.updated_at,
                    )
                )

            return conversations

    async def get_conversation(
        self,
        conversation_id: str,
    ) -> ConversationHistory:
        """
        Return all messages stored for a conversation.
        """
        async with AsyncSessionFactory() as session:
            statement = (
                select(ChatMessageModel)
                .where(
                    ChatMessageModel.conversation_id
                    == conversation_id
                )
                .order_by(
                    ChatMessageModel.created_at.asc()
                )
            )

            result = await session.execute(
                statement
            )

            models = result.scalars().all()

        messages = [
            ChatMessage(
                conversation_id=model.conversation_id,
                role=MessageRole(model.role),
                content=model.content,
                created_at=model.created_at,
            )
            for model in models
        ]

        return ConversationHistory(
            conversation_id=conversation_id,
            messages=messages,
        )

    async def _get_title(
        self,
        session,
        conversation_id: str,
    ) -> str:
        """
        Build a conversation title from the first user message.
        """
        statement = (
            select(
                ChatMessageModel.content
            )
            .where(
                ChatMessageModel.conversation_id
                == conversation_id,
                ChatMessageModel.role
                == MessageRole.USER.value,
            )
            .order_by(
                ChatMessageModel.created_at.asc()
            )
            .limit(1)
        )

        result = await session.execute(
            statement
        )

        content = result.scalar_one_or_none()

        if not content:
            return "Nova conversa"

        cleaned = (
            content.replace("\n", " ")
            .strip()
        )

        if len(cleaned) <= 42:
            return cleaned

        return (
            cleaned[:42].rstrip()
            + "..."
        )