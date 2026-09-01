import httpx
import streamlit as st

from frontend.services.api_client import (
    download_summary_document,
    generate_conversation_summary,
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
        summary = generate_conversation_summary(
            conversation_id
        )

        st.session_state[
            f"{area}_summary"
        ] = summary

        progress.progress(
            35,
            text="Resumo preparado. Gerando PDF...",
        )

        pdf = download_summary_document(
            conversation_id=conversation_id,
            document_format="pdf",
        )

        st.session_state[
            f"{area}_summary_pdf"
        ] = pdf

        progress.progress(
            70,
            text="PDF pronto. Gerando DOCX...",
        )

        docx = download_summary_document(
            conversation_id=conversation_id,
            document_format="docx",
        )

        st.session_state[
            f"{area}_summary_docx"
        ] = docx

        progress.progress(
            100,
            text="Material pronto!",
        )

        st.success(
            "Resumo e arquivos preparados com sucesso."
        )

    except httpx.RequestError:
        st.error(
            "Não foi possível conectar ao servidor."
        )

    except httpx.HTTPStatusError:
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
                data=pdf,
                file_name="resumo_raissa_ai.pdf",
                mime="application/pdf",
                key=f"{area}_download_pdf",
                use_container_width=True,
            )

    with col2:
        if docx:
            st.download_button(
                label="📝 Baixar DOCX",
                data=docx,
                file_name="resumo_raissa_ai.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
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