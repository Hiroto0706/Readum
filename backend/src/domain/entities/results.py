import inspect
from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.entities.question import QuizOption
from src.domain.entities.quiz import Quiz


class UserAnswer(BaseModel):
    id: str = Field(..., description="Quizを識別するための一意のID")
    preview: Quiz = Field(..., description="クイズのプレビュー")
    selected_options: List[str] = Field(
        ..., description="ユーザーの選択した回答のリスト（A, B, C, D...）"
    )

    model_config = ConfigDict(frozen=True)

    @field_validator("selected_options")
    def validate_selected_options(cls, v, values):
        """
        回答の数がクイズの数と一致する
        各回答がA,B,C,Dのいずれかであることを保証する
        """
        if "preview" in values and len(v) != len(values["preview"].questions):
            raise ValueError(
                f"選択された回答の数({len(v)})がクイズの問題数({len(values['preview'].questions)})と一致しません"
            )

        valid_options = set(inspect.signature(QuizOption).parameters.keys())
        invalid_options = [opt for opt in v if opt not in valid_options]

        if invalid_options:
            raise ValueError(
                f"無効な回答が含まれています: {invalid_options}. 有効な回答は {', '.join(valid_options)} のみです"
            )

        return v
