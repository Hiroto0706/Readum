from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class QuestionCount:
    value: int = Field(..., description="生成するクイズの数", ge=3, le=20)
