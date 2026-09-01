import streamlit as st

from frontend.components.chat import render_chat


def render() -> None:
    """
    Render the finance assistant tab.
    """
    st.html(
        """
        <div class="raissa-card">
            <div class="card-title">
                💗 Cuide da sua vida financeira
            </div>

            <div class="card-description">
                Organize seus gastos, planeje metas
                e entenda melhor seu dinheiro.
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("💸 Gastos")

    with col2:
        st.caption("🎯 Metas")

    with col3:
        st.caption("🌱 Planejamento")

    render_chat(
        area="finance",
        placeholder="Vamos organizar suas finanças? 💕",
    )