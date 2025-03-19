from typing import Annotated
from pydantic import Field, constr
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class QuizContent:
    value: Annotated[str, constr(strip_whitespace=True, min_length=1)] = Field(
        ...,
        description="クイズの内容。空文字やホワイトスペースのみの文字列は許可されません。",
    )
