class QuizSubmitBaseException(Exception):
    """クイズの保存に関連する基底例外クラス"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class SaveObjectToStorageError(QuizSubmitBaseException):
    """Storageにオブジェクトを保存する処理中のエラー"""

    pass
