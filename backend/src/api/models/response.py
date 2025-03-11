from typing import List
from pydantic import BaseModel, Field


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
    questions: List[Quiz] = Field(
        ..., description="クイズのリスト", min_length=3, max_length=20
    )


class QuizResponse(BaseModel):
    preview: QuizPreview = Field(..., description="クイズのプレビュー")
