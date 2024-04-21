from hashlib import sha256
from typing import TYPE_CHECKING
from sqlalchemy import select

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )

    async def get_by_email(self, email: str) -> AdminModel | None:
        self.logger.info(f"Ищем по емейлу: {email}")
        async with self.app.database.session() as session:
            query = select(AdminModel).where(AdminModel.email == email)
            admin = await session.scalar(query)
        return admin

    async def create_admin(self, email: str, password: str) -> AdminModel:
        self.logger.info("Создаем админа")
        admin = AdminModel(
            email=email,
            password=sha256(password.encode()).hexdigest()
        )
        async with self.app.database.session() as session:
            exist_admin = await self.get_by_email(admin.email)
            if exist_admin is None:
                self.logger.info(f"Добавляем админа {admin.email}")
                session.add(admin)
                await session.commit()
            else:
                self.logger.warn(f"Пользователь {admin.email} уже существует  ")
                return admin
        return admin
