from typing import List
from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.domain.entities.question import Question


class Quiz(BaseModel):
    questions: List[Question] = Field(
        description="Questionのリスト。3問から10問の範囲でQuestionが生成されます"
    )

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def validate_question_count(self):
        if len(self.questions) < 3 or len(self.questions) > 10:
            raise ValueError("質問は3問から10問の範囲である必要があります")
        return self
