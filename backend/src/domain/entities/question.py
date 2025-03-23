from enum import Enum
from urllib.parse import urlparse
from pydantic import Field
from pydantic.dataclasses import dataclass


class QuizType(Enum):
    TEXT = "text"
    URL = "url"


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

    def __post_init__(self):
        """
        content が空でないことと、type が QuizType.URL の場合に有効な URL 形式かチェックします。
        """
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("The 'content' field cannot be empty.")

        if self.type == QuizType.URL:
            parsed = urlparse(self.content)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(
                    "When the 'type' field is set to 'url', the 'content' field must be in a valid URL format."
                )
