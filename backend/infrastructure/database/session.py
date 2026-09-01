from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import get_settings


def build_async_database_url(database_url: str) -> str:
    """
    Convert a PostgreSQL connection URL to the asyncpg SQLAlchemy format.
    """
    async_url = database_url.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1,
    )

    async_url = async_url.replace(
        "sslmode=require",
        "ssl=require",
    )

    async_url = async_url.replace(
        "&channel_binding=require",
        "",
    )

    return async_url


settings = get_settings()

ASYNC_DATABASE_URL = build_async_database_url(
    settings.database_url
)

engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)