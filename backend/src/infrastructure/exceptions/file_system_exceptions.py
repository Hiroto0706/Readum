class FileBaseException(Exception):
    """ファイル操作関連の基底例外クラス"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DirectoryCreationError(FileBaseException):
    """ディレクトリ作成時に発生するエラー"""

    pass


class DirectoryDeletionError(FileBaseException):
    """ディレクトリ削除時に発生するエラー"""

    pass
