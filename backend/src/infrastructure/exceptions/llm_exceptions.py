from pydantic.dataclasses import dataclass


@dataclass
class LLMBaseException(Exception):
    """LLM関連の処理で発生する基底例外クラス"""

    message: str

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class TranslationError(LLMBaseException):
    """テキスト変換処理中に発生するエラー"""

    pass


@dataclass
class DocumentLoadError(LLMBaseException):
    """ドキュメント読み込み処理中に発生するエラー"""

    pass


@dataclass
class DocumentSplitException(LLMBaseException):
    """ドキュメント分割処理中に発生するエラー"""

    pass


@dataclass
class SetUpRagChainError(LLMBaseException):
    """RAGチェーンの初期設定中に発生するエラー"""

    pass


@dataclass
class RagChainExecutionError(LLMBaseException):
    """RAGチェーンの実行中に発生するエラー"""

    pass


@dataclass
class RAGChainSetupError(LLMBaseException):
    """RAGチェーンの設定中に発生するエラー"""

    pass


@dataclass
class RAGChainExecutionError(LLMBaseException):
    """RAGチェーンの実行中に発生するエラー"""

    pass


@dataclass
class LLMResponseParsingError(LLMBaseException):
    """LLMの応答解析中に発生するエラー"""

    pass


@dataclass
class InvalidParameterError(LLMBaseException):
    """無効なパラメータが指定された場合のエラー"""

    pass
