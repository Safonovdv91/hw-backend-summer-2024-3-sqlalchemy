from aiohttp_apispec import querystring_schema, request_schema, response_schema
from aiohttp.web_exceptions import HTTPBadRequest, HTTPConflict, HTTPNotFound

from app.quiz.models import AnswerModel
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        theme_title = self.data["title"]
        if await self.store.quizzes.get_theme_by_title(theme_title):
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(theme_title)

        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()

        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        theme_id = self.data["theme_id"]
        raw_answers = self.data["answers"]
        title = self.data["title"]

        if len(raw_answers) < 2:
            raise HTTPBadRequest

        if await self.store.quizzes.get_theme_by_title(title):
            raise HTTPConflict

        if not await self.store.quizzes.get_theme_by_id(theme_id):
            raise HTTPNotFound

        answers = [
            AnswerModel(
                title=answer_raw["title"],
                is_correct=answer_raw["is_correct"])
            for answer_raw in raw_answers
        ]
        correct_answers = [answer for answer in answers if answer.is_correct]
        if len(correct_answers) != 1:
            raise HTTPBadRequest
        question = await self.store.quizzes.create_question(
            theme_id=theme_id,
            answers=answers,
            title=title
        )
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = self.request.query.get("theme_id")
        questions = await self.store.quizzes.list_questions(theme_id)

        return json_response(data=ListQuestionSchema().dump({"questions": questions}))
