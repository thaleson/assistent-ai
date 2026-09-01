import streamlit as st

from frontend.components.chat import render_chat


def render() -> None:
    """
    Render the general assistant tab.
    """
    st.html(
        """
        <div class="raissa-card">
            <div class="card-title">
                🌸 Converse comigo
            </div>

            <div class="card-description">
                Pode falar sobre seu dia, pedir ideias,
                organizar sua rotina ou simplesmente conversar.
            </div>
        </div>
        """
    )

    render_chat(
        area="general",
        placeholder="Me conta, como posso te ajudar? 🌷",
    )