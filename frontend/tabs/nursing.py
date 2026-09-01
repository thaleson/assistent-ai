import streamlit as st

from frontend.components.chat import render_chat


def render() -> None:
    """
    Render the nursing assistant tab.
    """
    st.html(
        """
        <div class="raissa-card">
            <div class="card-title">
                🩺 Enfermagem
            </div>

            <div class="card-description">
                Estude conteúdos de enfermagem, revise matérias,
                tire dúvidas e pratique com exercícios.
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("🫀 Anatomia")

    with col2:
        st.caption("📝 Resumos")

    with col3:
        st.caption("🧠 Exercícios")

    render_chat(
        area="nursing",
        placeholder="O que vamos estudar hoje? 🩺",
    )