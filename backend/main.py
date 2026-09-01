from fastapi import FastAPI

from backend.presentation.api.routes.chat import (
    router as chat_router,
)
from backend.presentation.api.routes.health import (
    router as health_router,
)

from backend.presentation.api.routes.conversations import (
    router as conversations_router,
)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    application = FastAPI(
        title="Raissa AI ",
        description="for the Raissa AI personal assistant.",
        version="0.1.0",
    )

    application.include_router(
        health_router,
        prefix="/api/v1",
    )

    application.include_router(
        chat_router,
        prefix="/api/v1",
    )

    application.include_router(
    conversations_router,
    prefix="/api/v1",
    )

    return application


app = create_app()