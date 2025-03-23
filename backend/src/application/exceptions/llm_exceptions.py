from pydantic.dataclasses import dataclass


@dataclass
class LLMExceptions(Exception):
    """LLMサービスの処理で発生したエラーを処理するクラス"""

    pass
