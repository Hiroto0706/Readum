from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class QuizOption:
    A: str
    B: str
    C: str
    D: str


@dataclass(frozen=True)
class Question:
    content: str = Field(..., description="質問内容")
    options: QuizOption = Field(..., description="選択肢")
    answer: str = Field(..., description="正解の選択肢")
    explanation: str = Field(..., description="解答の説明")
