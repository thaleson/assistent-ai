from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from frontend.components.layout import (
    load_css,
    render_footer,
    render_header,
    render_mobile_menu,
    render_sidebar,
)
from frontend.state.session import initialize_session
from frontend.tabs import (
    beauty,
    finance,
    general,
    nursing,
)


def main() -> None:
    """
    Run the Raissa AI Streamlit application.
    """
    st.set_page_config(
        page_title="Raissa AI",
        page_icon="🌷",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    load_css()
    initialize_session()

    render_sidebar()
    render_header()
    render_mobile_menu()

    (
        general_tab,
        nursing_tab,
        beauty_tab,
        finance_tab,
    ) = st.tabs(
        [
            "🌷 Raissa",
            "🩺 Enfermagem",
            "💇‍♀️ Salão & Beleza",
            "💰 Finanças",
        ]
    )

    with general_tab:
        general.render()

    with nursing_tab:
        nursing.render()

    with beauty_tab:
        beauty.render()

    with finance_tab:
        finance.render()

    render_footer()


if __name__ == "__main__":
    main()