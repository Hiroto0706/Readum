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
