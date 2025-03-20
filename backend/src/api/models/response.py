from typing import List
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Options:
    A: str
    B: str
    C: str
    D: str


@dataclass(frozen=True)
class Question:
    content: str = Field(..., description="質問内容")
    options: Options = Field(..., description="選択肢")
    answer: str = Field(..., description="正解の選択肢")
    explanation: str = Field(..., description="解答の説明")


@dataclass(frozen=True)
class Quiz:
    questions: List[Question] = Field(
        ..., description="クイズのリスト", min_length=3, max_length=20
    )


@dataclass(frozen=True)
class QuizResponse:
    id: str = Field(..., description="Quizを識別するための一意のID")
    preview: Quiz = Field(..., description="クイズのプレビュー")
