from enum import Enum
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    content: str = Field(..., description="質問内容")
    options: QuizOption = Field(..., description="選択肢")
    answer: str = Field(..., description="正解の選択肢")
    explanation: str = Field(..., description="解答の説明")

    model_config = ConfigDict(frozen=True)
