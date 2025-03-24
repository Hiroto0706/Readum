from pydantic.dataclasses import dataclass


@dataclass
class FileBaseException(Exception):
    """ファイル操作関連の基底例外クラス"""

    message: str

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class DirectoryCreationError(FileBaseException):
    """ディレクトリ作成時に発生するエラー"""

    pass


@dataclass
class DirectoryDeletionError(FileBaseException):
    """ディレクトリ削除時に発生するエラー"""

    pass
