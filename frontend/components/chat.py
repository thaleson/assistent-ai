import httpx
import streamlit as st

from frontend.services.api_client import send_message
from frontend.components.conversation_export import (
    render_conversation_export,
)


AREA_CONTEXTS = {
    "general": "",
    "nursing": (
        "Contexto da área atual: enfermagem e estudos. "
        "Priorize explicações didáticas, revisão de conteúdo, "
        "resumos, exercícios e aprendizado relacionado à enfermagem."
    ),
    "beauty": (
        "Contexto da área atual: salão de beleza. "
        "Priorize organização do salão, atendimento, serviços, "
        "preços, ideias de divulgação e rotina de beleza."
    ),
    "finance": (
        "Contexto da área atual: finanças pessoais. "
        "Priorize organização financeira, gastos, metas e planejamento."
    ),
}


def render_messages(
    area: str,
) -> None:
    """
    Render the messages stored for an assistant area.
    """
    messages = st.session_state[
        f"{area}_messages"
    ]

    for message in messages:
        avatar = (
            "🌷"
            if message["role"] == "assistant"
            else "✨"
        )

        with st.chat_message(
            message["role"],
            avatar=avatar,
        ):
            st.markdown(
                message["content"]
            )

            agent = message.get(
                "agent"
            )

            if agent:
                st.html(
                    (
                        '<div class="agent-label">'
                        f"Agente · {agent}"
                        "</div>"
                    )
                )


def build_contextual_message(
    area: str,
    user_message: str,
) -> str:
    """
    Build the message sent to the backend with area-specific context.
    """
    area_context = AREA_CONTEXTS.get(
        area,
        "",
    )

    if not area_context:
        return user_message

    return (
        f"{area_context}\n\n"
        f"Mensagem da usuária:\n{user_message}"
    )


def process_message(
    area: str,
    user_message: str,
) -> None:
    """
    Process a user message and render the assistant response.
    """
    messages_key = (
        f"{area}_messages"
    )

    st.session_state[
        messages_key
    ].append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message(
        "user",
        avatar="✨",
    ):
        st.markdown(
            user_message
        )

    with st.chat_message(
        "assistant",
        avatar="🌷",
    ):
        with st.spinner(
            "Raissa está pensando..."
        ):
            try:
                contextual_message = build_contextual_message(
                    area=area,
                    user_message=user_message,
                )

                response = send_message(
                    message=contextual_message,
                    conversation_id=(
                        st.session_state[
                            f"{area}_conversation_id"
                        ]
                    ),
                )

                assistant_message = (
                    response["message"]
                )

                agent = response[
                    "agent"
                ]

                st.markdown(
                    assistant_message
                )

                st.html(
                    (
                        '<div class="agent-label">'
                        f"Agente · {agent}"
                        "</div>"
                    )
                )

                st.session_state[
                    messages_key
                ].append(
                    {
                        "role": "assistant",
                        "content": assistant_message,
                        "agent": agent,
                    }
                )

            except httpx.HTTPStatusError:
                st.error(
                    "O servidor não conseguiu "
                    "processar sua mensagem."
                )

            except httpx.RequestError:
                st.error(
                    "Não foi possível conectar "
                    "à Raissa AI."
                )


def render_chat(
    area: str,
    placeholder: str,
) -> None:
    """
    Render an independent chat for the selected area.
    """
    render_messages(
        area
    )

    render_conversation_export(
        area
    )

    user_message = st.chat_input(
        placeholder,
        key=f"{area}_chat_input",
    )

    if user_message:
        process_message(
            area=area,
            user_message=user_message,
        )

        st.rerun()