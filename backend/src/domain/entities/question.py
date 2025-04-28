from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class QuizType(Enum):
    TEXT = "text"
    URL = "url"


class QuizOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

    model_config = ConfigDict(frozen=True)


class Question(BaseModel):
    content: str = Field(..., description="質問内容", alias="question")
    options: QuizOption = Field(..., description="選択肢")
    answer: str = Field(..., description="正解の選択肢", alias="correctAnswer")
    explanation: str = Field(..., description="解答の説明")

    model_config = ConfigDict(frozen=True, populate_by_name=True)
