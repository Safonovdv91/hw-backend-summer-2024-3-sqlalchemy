from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String[300], unique=True, index=True)

    questions: Mapped[List["QuestionModel"]] = relationship(back_populates="theme", cascade="all, delete-orphan")


class QuestionModel(BaseModel):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String[300], unique=True)

    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    theme: Mapped["ThemeModel"] = relationship(back_populates="questions")

    answers: Mapped[List["AnswerModel"]] = relationship(back_populates="question", cascade="all, delete-orphan")


class AnswerModel(BaseModel):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String[300], unique=True)
    is_correct: Mapped[bool] = mapped_column(Boolean)

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    question: Mapped["QuestionModel"] = relationship(back_populates="answers")

