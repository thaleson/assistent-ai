import streamlit as st

from frontend.components.chat import render_chat


def render() -> None:
    """
    Render the beauty and salon assistant tab.
    """
    st.html(
        """
        <div class="raissa-card">
            <div class="card-title">
                💇‍♀️ Salão & Beleza
            </div>

            <div class="card-description">
                Organize serviços, preços e ideias para o salão,
                além de receber ajuda com rotina e divulgação.
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("✂️ Serviços")

    with col2:
        st.caption("📅 Organização")

    with col3:
        st.caption("💅 Ideias")

    render_chat(
        area="beauty",
        placeholder="Como posso ajudar no salão hoje? 💇‍♀️",
    )