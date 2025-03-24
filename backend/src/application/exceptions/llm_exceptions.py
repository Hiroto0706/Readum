from pydantic.dataclasses import dataclass


@dataclass
class QuizCreationBaseException(Exception):
    """クイズ作成に関連する基底例外クラス"""

    message: str

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class DocumentProcessingError(QuizCreationBaseException):
    """ドキュメント処理中のエラー"""

    pass


@dataclass
class VectorStoreOperationError(QuizCreationBaseException):
    """ベクトルストア操作中のエラー"""

    pass


@dataclass
class RAGProcessingError(QuizCreationBaseException):
    """RAG処理中のエラー"""

    pass


@dataclass
class InvalidInputError(QuizCreationBaseException):
    """無効な入力パラメータのエラー"""

    pass
