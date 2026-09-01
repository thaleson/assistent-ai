import streamlit as st

from frontend.components.chat import render_chat


def render() -> None:
    """
    Render the study assistant tab.
    """
    st.html(
        """
        <div class="raissa-card">
            <div class="card-title">
                📚 Hora de estudar
            </div>

            <div class="card-description">
                Tire dúvidas, peça explicações, exercícios,
                resumos ou monte seu plano de estudos.
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("📝 Explicações")

    with col2:
        st.caption("🧠 Exercícios")

    with col3:
        st.caption("🗓️ Planejamento")

    render_chat(
        area="study",
        placeholder="O que vamos estudar hoje? 📖",
    )