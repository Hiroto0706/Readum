from pydantic import Field
from pydantic.dataclasses import dataclass

from src.api.models.request import QuizType
from src.domain.value_objects.question_count import QuestionCount
from src.domain.value_objects.quiz_content import QuizContent
from src.domain.value_objects.quiz_difficulty import QuizDifficulty


@dataclass(frozen=True)
class Question:
    content: QuizContent = Field(..., description="クイズの内容")
    quiz_type: QuizType = Field(..., description="クイズのタイプ（text または url）")
    difficulty: QuizDifficulty = Field(
        ..., description="クイズの難易度（beginner, intermediate, advanced）"
    )
    question_count: QuestionCount = Field(..., description="生成するクイズの数")
