from typing import List
from enum import Enum
from urllib.parse import urlparse
from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


class QuizType(Enum):
    TEXT = "text"
    URL = "url"


class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass(config=ConfigDict(populate_by_name=True))
class QuizRequest:
    type: QuizType = Field(..., description="クイズのタイプ（テキスト or URL）")
    content: str = Field(
        ..., description="ユーザーからの入力内容（読書メモやテストしたいサイトのURL）"
    )
    difficulty: Difficulty = Field(..., description="クイズの難易度")
    question_count: int = Field(
        ..., alias="questionCount", description="生成するクイズの数", ge=3, le=20
    )

    def __post_init__(self):
        """
        type が QuizType.URL の場合、content が有効な URL 形式かチェックします。
        """
        if self.type == QuizType.URL:
            parsed = urlparse(self.content)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(
                    "When the 'type' field is set to 'url', the 'content' field must be in a valid URL format."
                )


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
