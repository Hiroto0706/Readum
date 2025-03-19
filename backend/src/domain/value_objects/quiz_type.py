from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass


class QuizTypeEnum(Enum):
    TEXT = "text"
    URL = "url"


@dataclass(frozen=True)
class QuizType:
    value: QuizTypeEnum = Field(
        ..., description="クイズのタイプ。'text' または 'url' が指定できます。"
    )
