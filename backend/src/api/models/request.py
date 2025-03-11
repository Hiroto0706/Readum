from enum import Enum
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuizType(Enum):
    TEXT = "text"
    URL = "url"


class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class QuizRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: QuizType = Field(..., description="クイズのタイプ（テキスト or URL）")
    content: str = Field(
        ..., description="ユーザーからの入力内容（読書メモやテストしたいサイトのURL）"
    )
    difficulty: Difficulty = Field(..., description="クイズの難易度")
    question_count: int = Field(
        ..., alias="questionCount", description="生成するクイズの数", ge=3, le=20
    )

    @field_validator("content")
    def validate_content_for_url(cls, v: str, info) -> str:
        type_value = info.data.get("type")
        if type_value == QuizType.URL:
            parsed = urlparse(v)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(
                    "When the 'type' field is set to 'url', the 'content' field must be in a valid URL format."
                )
        return v
