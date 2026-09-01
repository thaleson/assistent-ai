import asyncio
import threading
from collections.abc import Coroutine
from typing import Any, TypeVar

import streamlit as st


T = TypeVar("T")


class AsyncRunner:
    """
    Execute asynchronous operations on a persistent background event loop.
    """

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()

        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True,
            name="raissa-ai-async-loop",
        )

        self._thread.start()

    def _run_loop(self) -> None:
        """
        Run the dedicated event loop forever in the background thread.
        """
        asyncio.set_event_loop(
            self._loop
        )

        self._loop.run_forever()

    def run(
        self,
        coroutine: Coroutine[Any, Any, T],
    ) -> T:
        """
        Execute a coroutine on the dedicated background event loop.
        """
        future = asyncio.run_coroutine_threadsafe(
            coroutine,
            self._loop,
        )

        return future.result()


@st.cache_resource
def get_async_runner() -> AsyncRunner:
    """
    Return the shared asynchronous runner.
    """
    return AsyncRunner()


def run_async(
    coroutine: Coroutine[Any, Any, T],
) -> T:
    """
    Execute an asynchronous operation using the shared runner.
    """
    runner = get_async_runner()

    return runner.run(
        coroutine
    )