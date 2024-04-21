from typing import TYPE_CHECKING, Any
from sqlalchemy.orm import declarative_base

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from app.store.database import BaseModel

if TYPE_CHECKING:
    from app.web.app import Application
    from app.admin.models import AdminModel


class Database:
    def __init__(self, app: "Application") -> None:
        self.app = app

        self.engine: AsyncEngine | None = None
        self._db: type[DeclarativeBase] = BaseModel
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        host: str = self.app.config.database.host
        port: int = self.app.config.database.port
        user: str = self.app.config.database.user
        password: str = self.app.config.database.password
        database: str = self.app.config.database.database

        self.engine = create_async_engine(
            url=f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}",
            echo=True,
            future=True
        )
        # async_session_maker = async_sessionmaker(
        #     self.engine, class_=AsyncSession, expire_on_commit=False
        # )
        self.session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        # self.engine = create_async_engine(
        #     URL.create(
        #     ),
        # )
        # self.session = async_sessionmaker(
        #
        # )

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        pass
