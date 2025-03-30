class LLMBaseException(Exception):
    """LLM関連の処理で発生する基底例外クラス"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TranslationError(LLMBaseException):
    """テキスト変換処理中に発生するエラー"""

    pass


class DocumentLoadError(LLMBaseException):
    """ドキュメント読み込み処理中に発生するエラー"""

    pass


class DocumentSplitException(LLMBaseException):
    """ドキュメント分割処理中に発生するエラー"""

    pass


class SetUpRagChainError(LLMBaseException):
    """RAGチェーンの初期設定中に発生するエラー"""

    pass


class RagChainExecutionError(LLMBaseException):
    """RAGチェーンの実行中に発生するエラー"""

    pass


class RAGChainSetupError(LLMBaseException):
    """RAGチェーンの設定中に発生するエラー"""

    pass


class RAGChainExecutionError(LLMBaseException):
    """RAGチェーンの実行中に発生するエラー"""

    pass


class LLMResponseParsingError(LLMBaseException):
    """LLMの応答解析中に発生するエラー"""

    pass


class InvalidParameterError(LLMBaseException):
    """無効なパラメータが指定された場合のエラー"""

    pass
