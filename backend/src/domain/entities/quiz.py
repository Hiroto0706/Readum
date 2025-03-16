"""
クイズに関するEntity
"""

from typing import List
from pydantic import Field
from pydantic.dataclasses import dataclass

from src.domain.value_objects.quiz_content import (
    QuestionCount,
    QuizContent,
    QuizDifficulty,
    QuizType,
)


@dataclass(frozen=True)
class Quiz:
    id: str = Field(..., description="クイズの一意な識別子")
    content: QuizContent = Field(..., description="クイズの内容")
    quiz_type: QuizType = Field(..., description="クイズのタイプ（text または url）")
    difficulty: QuizDifficulty = Field(
        ..., description="クイズの難易度（beginner, intermediate, advanced）"
    )
    question_count: QuestionCount = Field(..., description="生成するクイズの数")


@dataclass(frozen=True)
class QuizPreview:
    questions: List[Quiz] = Field(
        ..., description="クイズのリスト", min_length=3, max_length=20
    )
