from pydantic.dataclasses import dataclass


@dataclass
class EmbeddingsExceptions(Exception):
    """Embeddingsサービスの処理で発生したエラーを処理するクラス"""

    pass
