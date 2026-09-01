import httpx
import streamlit as st

from frontend.services.api_client import (
    get_conversation,
    list_conversations,
)
from frontend.state.session import (
    load_conversation,
)


def _clean_message_content(
    content: str,
) -> str:
    """
    Remove internal area context from messages displayed to the user.
    """
    marker = "Mensagem da usuária:\n"

    if marker in content:
        return content.split(
            marker,
            maxsplit=1,
        )[1].strip()

    return content


def _clean_title(
    title: str,
) -> str:
    """
    Clean internal context from conversation titles.
    """
    if title.startswith(
        "Contexto da área atual:"
    ):
        return "Conversa de estudos"

    return title


def _convert_messages(
    backend_messages: list[dict],
) -> list[dict]:
    """
    Convert backend messages into Streamlit chat messages.
    """
    messages: list[dict] = []

    for message in backend_messages:
        messages.append(
            {
                "role": message["role"],
                "content": _clean_message_content(
                    message["content"]
                ),
            }
        )

    return messages


def open_conversation(
    conversation_id: str,
) -> None:
    """
    Load a selected conversation from the backend.
    """
    conversation = get_conversation(
        conversation_id
    )

    messages = _convert_messages(
        conversation["messages"]
    )

    load_conversation(
        conversation_id=conversation_id,
        messages=messages,
    )


def render_conversation_history() -> None:
    """
    Render clickable recent conversations in the sidebar.
    """
    st.markdown("### 🕘 Chats Recentes")

    try:
        conversations = list_conversations()

    except httpx.RequestError:
        st.caption(
            "Não foi possível carregar o histórico."
        )
        return

    except httpx.HTTPStatusError:
        st.caption(
            "Erro ao carregar o histórico."
        )
        return

    if not conversations:
        st.caption(
            "Nenhuma conversa ainda."
        )
        return

    for conversation in conversations[:15]:
        conversation_id = conversation[
            "conversation_id"
        ]

        title = _clean_title(
            conversation["title"]
        )

        if st.button(
            title,
            key=f"history_{conversation_id}",
            use_container_width=True,
        ):
            try:
                open_conversation(
                    conversation_id
                )

                st.rerun()

            except httpx.RequestError:
                st.error(
                    "Não foi possível abrir essa conversa."
                )

            except httpx.HTTPStatusError:
                st.error(
                    "Essa conversa não pôde ser carregada."
                )