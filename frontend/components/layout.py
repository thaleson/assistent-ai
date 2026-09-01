from pathlib import Path

import streamlit as st

from frontend.state.session import clear_conversation

from frontend.components.conversation_history import (
    render_conversation_history,
)

def load_css() -> None:
    """
    Load the application stylesheet.
    """
    css_path = (
        Path(__file__).resolve().parents[1]
        / "styles.css"
    )

    css = css_path.read_text(
        encoding="utf-8"
    )

    st.html(
        f"<style>{css}</style>"
    )


def render_header() -> None:
    """
    Render the main Raissa AI header.
    """
    st.html(
        """
        <div class="raissa-header">
            <div class="raissa-badge">
                ✨ Sua assistente pessoal
            </div>

            <div class="raissa-logo">
                Raissa AI 🌷
            </div>

            <div class="raissa-subtitle">
                Conversas, estudos e finanças em um só lugar.
            </div>
        </div>
        """
    )


def render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    
    with st.sidebar:
        st.html(
            """
            <div class="sidebar-brand">
                Raissa AI 🌷
            </div>

            <div class="sidebar-subtitle">
                Sua assistente pessoal,
                sempre pertinho de você.
            </div>
            """
        )

        st.markdown(
            "### ✨ Conversas"
        )

        if st.button(
            "🌷 Nova conversa",
            use_container_width=True,
        ):
            clear_conversation(
                "general"
            )
            st.rerun()
            

        if st.button(
            "🩺 Novo estudo",
            use_container_width=True,
        ):
            clear_conversation(
                "nursing"
            )
            st.rerun()

        if st.button(
            "💇‍♀️ Novo salão",
            use_container_width=True,
        ):
            clear_conversation(
                "beauty"
            )
            st.rerun()

        if st.button(
            "💰 Novo planejamento",
            use_container_width=True,
        ):
            clear_conversation(
                "finance"
            )
            st.rerun()

        st.divider()

        render_conversation_history(
            key_prefix="sidebar_history"
        )

        st.divider()

        st.caption(
            "Suas conversas são salvas automaticamente."
        )


def render_footer() -> None:
    """
    Render the application footer.
    """
    st.html(
        """
        <div class="raissa-footer">
            Feito com carinho para tornar sua rotina mais leve. 🌷
        </div>
        """
    )


def render_mobile_menu() -> None:
    """
    Render the main application navigation menu.
    """

    with st.popover(
        "☰ Menu",
        use_container_width=False,
    ):
        st.markdown("### 🌷 Raissa AI")

        st.caption(
            "Conversas, estudos e organização."
        )

        if st.button(
            "🌷 Nova conversa",
            use_container_width=True,
            key="mobile_new_general",
        ):
            clear_conversation("general")
            st.rerun()

        if st.button(
            "🩺 Novo estudo",
            use_container_width=True,
            key="mobile_new_nursing",
        ):
            clear_conversation("nursing")
            st.rerun()

        if st.button(
            "💇‍♀️ Novo salão",
            use_container_width=True,
            key="mobile_new_beauty",
        ):
            clear_conversation("beauty")
            st.rerun()

        if st.button(
            "💰 Novo planejamento",
            use_container_width=True,
            key="mobile_new_finance",
        ):
            clear_conversation("finance")
            st.rerun()

        st.divider()

        render_conversation_history(
                    key_prefix="mobile_history"
                )  