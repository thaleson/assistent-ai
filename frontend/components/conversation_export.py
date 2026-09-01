import streamlit as st

from frontend.services.assistant_service import (
    prepare_conversation_material,
)


def _generate_material(
    area: str,
    conversation_id: str,
) -> None:
    """
    Generate the conversation summary and downloadable documents.
    """
    progress = st.progress(
        0,
        text="Preparando seu resumo...",
    )

    try:
        progress.progress(
            20,
            text="Analisando a conversa...",
        )

        material = prepare_conversation_material(
            conversation_id
        )

        progress.progress(
            55,
            text="Resumo pronto. Preparando PDF...",
        )

        st.session_state[
            f"{area}_summary"
        ] = material["summary"]

        st.session_state[
            f"{area}_summary_pdf"
        ] = material["pdf"]

        progress.progress(
            80,
            text="PDF pronto. Preparando DOCX...",
        )

        st.session_state[
            f"{area}_summary_docx"
        ] = material["docx"]

        progress.progress(
            100,
            text="Material pronto!",
        )

        st.success(
            "Resumo e arquivos preparados com sucesso."
        )

    except Exception:
        st.error(
            "Não foi possível preparar o material."
        )


def _render_downloads(
    area: str,
) -> None:
    """
    Render available document download buttons.
    """
    pdf = st.session_state.get(
        f"{area}_summary_pdf"
    )

    docx = st.session_state.get(
        f"{area}_summary_docx"
    )

    if not pdf and not docx:
        return

    col1, col2 = st.columns(2)

    with col1:
        if pdf:
            st.download_button(
                label="📄 Baixar PDF",
                data=pdf["content"],
                file_name=pdf["filename"],
                mime=pdf["media_type"],
                key=f"{area}_download_pdf",
                use_container_width=True,
            )

    with col2:
        if docx:
            st.download_button(
                label="📝 Baixar DOCX",
                data=docx["content"],
                file_name=docx["filename"],
                mime=docx["media_type"],
                key=f"{area}_download_docx",
                use_container_width=True,
            )


def render_conversation_export(
    area: str,
) -> None:
    """
    Render conversation summary and document download controls.
    """
    messages = st.session_state.get(
        f"{area}_messages",
        [],
    )

    if not messages:
        return

    conversation_id = st.session_state[
        f"{area}_conversation_id"
    ]

    st.divider()

    st.markdown(
        "### ✨ Resumo da conversa"
    )

    if st.button(
        "Preparar resumo e arquivos",
        key=f"{area}_generate_summary",
        use_container_width=True,
    ):
        _generate_material(
            area=area,
            conversation_id=conversation_id,
        )

    summary = st.session_state.get(
        f"{area}_summary"
    )

    if not summary:
        return

    st.markdown(
        summary["summary"]
    )

    _render_downloads(
        area
    )