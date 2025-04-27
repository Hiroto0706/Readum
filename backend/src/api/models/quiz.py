import inspect
from typing import List
from enum import Enum
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.domain.entities.quiz import Quiz as DomainQuiz


class QuizType(Enum):
    TEXT = "text"
    URL = "url"


class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class QuizRequest(BaseModel):
    type: QuizType = Field(..., description="クイズのタイプ（テキスト or URL）")
    content: str = Field(
        ..., description="ユーザーからの入力内容（読書メモやテストしたいサイトのURL）"
    )
    difficulty: Difficulty = Field(..., description="クイズの難易度")
    question_count: int = Field(
        ..., alias="questionCount", description="生成するクイズの数", ge=3, le=10
    )

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    @field_validator("content")
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        """content が空でないことをチェックします。"""
        if not v or len(v.strip()) == 0:
            raise ValueError("The 'content' field cannot be empty.")
        return v

    @model_validator(mode="after")
    def validate_content(self):
        """
        contentが空じゃない & type が QuizType.URL の場合、content が有効な URL 形式かチェック。
        """
        if self.type == QuizType.URL:
            parsed = urlparse(self.content)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(
                    "When the 'type' field is set to 'url', the 'content' field must be in a valid URL format."
                )
        return self


class Options(BaseModel):
    A: str
    B: str
    C: str
    D: str

    model_config = ConfigDict(frozen=True)


class Question(BaseModel):
    content: str = Field(..., description="質問内容")
    options: Options = Field(..., description="選択肢")
    answer: str = Field(..., description="正解の選択肢")
    explanation: str = Field(..., description="解答の説明")

    model_config = ConfigDict(frozen=True)


class Quiz(BaseModel):
    questions: List[Question] = Field(
        ..., description="クイズのリスト", min_length=3, max_length=10
    )

    model_config = ConfigDict(frozen=True)


class QuizResponse(BaseModel):
    id: str = Field(..., description="Quizを識別するための一意のID")
    preview: DomainQuiz = Field(..., description="クイズのプレビュー")
    difficulty_value: str = Field(description="クイズの難易度", alias="difficultyValue")

    model_config = ConfigDict(populate_by_name=True, frozen=True)


class UserAnswer(BaseModel):
    id: str = Field(..., description="Quizを識別するための一意のID")
    preview: Quiz = Field(..., description="クイズのプレビュー")
    selected_options: List[str] = Field(
        ...,
        description="ユーザーの選択した回答のリスト（A, B, C, D...）",
        alias="selectedOptions",
    )
    difficulty_value: str = Field(description="クイズの難易度", alias="difficultyValue")

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    @field_validator("selected_options")
    def validate_selected_options(cls, v, info):
        """
        回答の数がクイズの数と一致する
        各回答がA,B,C,Dのいずれかであることを保証する
        """
        preview: Quiz = info.data.get("preview")
        if preview and len(v) != len(preview.questions):
            raise ValueError(
                f"選択された回答の数({len(v)})がクイズの問題数({len(preview.questions)})と一致しません"
            )

        valid_options = set(inspect.signature(Options).parameters.keys())
        invalid_options = [opt for opt in v if opt not in valid_options]

        if invalid_options:
            raise ValueError(
                f"無効な回答が含まれています: {invalid_options}. 有効な回答は {', '.join(valid_options)} のみです"
            )

        return v
