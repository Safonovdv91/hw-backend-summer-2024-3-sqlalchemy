from collections.abc import Iterable, Sequence
from aiohttp.web_exceptions import HTTPForbidden
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        self.logger.info("Создаем тему")
        async with self.app.database.session() as session:
            theme = await self.get_theme_by_title(title)
            # if theme:
            #     self.logger.info("Тема уже существует")
            #     raise HTTPForbidden
            self.logger.info("Добавляем в базу данных")
            theme = ThemeModel(title=title)
            session.add(theme)
            await session.commit()
            return theme

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        self.logger.info("Получаем тему по заголовку")
        async with self.app.database.session() as session:
            query = select(ThemeModel).where(ThemeModel.title == title)
            theme = await session.scalar(query)
        return theme

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        self.logger.info("Получаем тему по id")
        async with self.app.database.session() as session:
            query = select(ThemeModel).where(ThemeModel.id == id_)
            theme = await session.scalar(query)
        return theme

    async def list_themes(self) -> Sequence[ThemeModel]:
        self.logger.info("Возвращаем все существующие темы")
        async with self.app.database.session() as session:
            result = await session.execute(select(ThemeModel))
            themes = result.scalars().all()
        return themes

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        async with self.app.database.session() as session:
            question = QuestionModel(
                title=title,
                theme_id=theme_id,
                answers=answers
            )
            session.add(question)
            await session.commit()
        return question

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        async with self.app.database.session() as session:
            query = select(QuestionModel).where(QuestionModel.title == title)
            question = await session.execute(query)
        return question.scalar()

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        async with self.app.database.session() as session:
            if theme_id is None:
                query = select(QuestionModel)
            else:
                query = select(QuestionModel).where(QuestionModel.theme_id == theme_id)

            questions = await session.execute(query.options(selectinload(QuestionModel.answers)))
        return questions.scalars().all()
