from pydantic.dataclasses import dataclass


@dataclass
class LLMExceptions(Exception):
    pass
