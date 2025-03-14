from enum import Enum
from pydantic import Field, constr
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class QuizContent:
    value: constr(strip_whitespace=True, min_length=1) = Field(
        ..., description="クイズの内容。空文字は許可されません。"
    )


class QuizTypeEnum(Enum):
    TEXT = "text"
    URL = "url"


@dataclass(frozen=True)
class QuizType:
    value: QuizTypeEnum = Field(
        ..., description="クイズのタイプ。'text' または 'url' が指定できます。"
    )


class QuizDifficultyEnum(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass(frozen=True)
class QuizDifficulty:
    value: QuizDifficultyEnum = Field(
        ...,
        description="クイズの難易度。'beginner', 'intermediate', 'advanced' のいずれかを指定します。",
    )


@dataclass(frozen=True)
class QuestionCount:
    value: int = Field(..., description="生成するクイズの数", ge=3, le=20)
