import uuid

import streamlit as st


AREAS = (
    "general",
    "nursing",
    "beauty",
    "finance",
)


def initialize_session() -> None:
    """
    Initialize independent conversation state for each assistant area.
    """
    for area in AREAS:
        conversation_key = f"{area}_conversation_id"
        messages_key = f"{area}_messages"

        if conversation_key not in st.session_state:
            st.session_state[conversation_key] = str(
                uuid.uuid4()
            )

        if messages_key not in st.session_state:
            st.session_state[messages_key] = []


def clear_conversation(
    area: str,
) -> None:
    """
    Start a new conversation for the selected assistant area.
    """
    st.session_state[
        f"{area}_conversation_id"
    ] = str(uuid.uuid4())

    st.session_state[
        f"{area}_messages"
    ] = []

    st.session_state.pop(
        f"{area}_summary",
        None,
    )

    st.session_state.pop(
        f"{area}_summary_pdf",
        None,
    )

    st.session_state.pop(
        f"{area}_summary_docx",
        None,
    )

def load_conversation(
    conversation_id: str,
    messages: list[dict],
) -> None:
    """
    Load an existing conversation into the main assistant area.
    """
    st.session_state[
        "general_conversation_id"
    ] = conversation_id

    st.session_state[
        "general_messages"
    ] = messages

    st.session_state.pop(
        "general_summary",
        None,
    )

    st.session_state.pop(
        "general_summary_pdf",
        None,
    )

    st.session_state.pop(
        "general_summary_docx",
        None,
    )