from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass


class QuizDifficultyEnum(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass(frozen=True)
class QuizDifficulty:
    value: QuizDifficultyEnum = Field(
        ...,
        description="クイズの難易度。'beginner', 'intermediate', 'advanced' のいずれかを指定します。",
    )
