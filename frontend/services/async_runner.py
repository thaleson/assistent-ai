import asyncio
from collections.abc import Coroutine
from typing import Any, TypeVar

import streamlit as st


T = TypeVar("T")


@st.cache_resource
def get_event_loop() -> asyncio.AbstractEventLoop:
    """
    Create and reuse a dedicated event loop for asynchronous services.
    """
    return asyncio.new_event_loop()


def run_async(
    coroutine: Coroutine[Any, Any, T],
) -> T:
    """
    Execute an asynchronous operation using the shared event loop.
    """
    loop = get_event_loop()

    return loop.run_until_complete(
        coroutine
    )