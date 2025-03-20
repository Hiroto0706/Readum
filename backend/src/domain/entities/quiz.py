"""
クイズに関するEntity
"""

from typing import List
from pydantic import Field
from pydantic.dataclasses import dataclass

from src.domain.entities.question import Question


@dataclass(frozen=True)
class Quiz:
    questions: List[Question] = Field(
        ..., description="クイズのリスト", min_length=3, max_length=20
    )
