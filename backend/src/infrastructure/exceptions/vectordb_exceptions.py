class VectorDBBaseException(Exception):
    """ベクトルデータベース操作に関連する基底例外クラス"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class VectorStoreCreationError(VectorDBBaseException):
    """ベクトルストアの作成時に発生するエラー"""

    pass


class VectorStoreSaveError(VectorDBBaseException):
    """ベクトルストアの保存時に発生するエラー"""

    pass


class VectorStoreLoadError(VectorDBBaseException):
    """ベクトルストアの読み込み時に発生するエラー"""

    pass


class VectorStoreNotInitializedError(VectorDBBaseException):
    """ベクトルストアが初期化されていない場合のエラー"""

    pass


class VectorStoreRetrievalError(VectorDBBaseException):
    """ベクトルストアからのデータ検索時に発生するエラー"""

    pass


class InvalidDocumentError(VectorDBBaseException):
    """無効なドキュメントが提供された場合のエラー"""

    pass
