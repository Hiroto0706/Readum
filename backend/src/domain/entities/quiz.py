from typing import List
import uuid
from pydantic import Field
from pydantic.dataclasses import dataclass

from src.domain.entities.question import Question


@dataclass(frozen=True)
class Quiz:
    id: str = uuid.uuid4().hex
    questions: List[Question] = Field(
        ..., description="Questionのリスト", min_length=3, max_length=20
    )
