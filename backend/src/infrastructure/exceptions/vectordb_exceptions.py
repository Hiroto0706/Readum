from pydantic.dataclasses import dataclass


@dataclass
class VectorDBBaseException(Exception):
    """ベクトルデータベース操作に関連する基底例外クラス"""

    message: str

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class VectorStoreCreationError(VectorDBBaseException):
    """ベクトルストアの作成時に発生するエラー"""

    pass


@dataclass
class VectorStoreSaveError(VectorDBBaseException):
    """ベクトルストアの保存時に発生するエラー"""

    pass


@dataclass
class VectorStoreLoadError(VectorDBBaseException):
    """ベクトルストアの読み込み時に発生するエラー"""

    pass


@dataclass
class VectorStoreNotInitializedError(VectorDBBaseException):
    """ベクトルストアが初期化されていない場合のエラー"""

    pass


@dataclass
class VectorStoreRetrievalError(VectorDBBaseException):
    """ベクトルストアからのデータ検索時に発生するエラー"""

    pass


@dataclass
class InvalidDocumentError(VectorDBBaseException):
    """無効なドキュメントが提供された場合のエラー"""

    pass
