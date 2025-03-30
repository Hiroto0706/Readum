class QuizCreationBaseException(Exception):
    """クイズ作成に関連する基底例外クラス"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DocumentProcessingError(QuizCreationBaseException):
    """ドキュメント処理中のエラー"""

    pass


class VectorStoreOperationError(QuizCreationBaseException):
    """ベクトルストア操作中のエラー"""

    pass


class RAGProcessingError(QuizCreationBaseException):
    """RAG処理中のエラー"""

    pass


class InvalidInputError(QuizCreationBaseException):
    """無効な入力パラメータのエラー"""

    pass
