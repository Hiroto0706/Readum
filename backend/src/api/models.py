from typing import List
from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    type: str = Field(..., description="クイズのタイプ（テキスト or URL）")
    content: str = Field(
        ..., description="ユーザーからの入力内容（読書メモやテストしたいサイトのURL）"
    )
    difficulty: str = Field(..., description="クイズの難易度")
    question_count: int = Field(
        ..., alias="questionCount", description="生成するクイズの数", ge=3, le=20
    )


class QuizOption(BaseModel):
    A: str
    B: str
    C: str
    D: str


class Quiz(BaseModel):
    content: str = Field(..., description="質問内容")
    options: QuizOption = Field(..., description="選択肢")
    answer: str = Field(..., description="正解の選択肢")
    explanation: str = Field(..., description="解答の説明")


class QuizPreview(BaseModel):
    questions: List[Quiz] = Field(..., description="クイズのリスト")


class QuizResponse(BaseModel):
    preview: QuizPreview = Field(..., description="クイズのプレビュー")
