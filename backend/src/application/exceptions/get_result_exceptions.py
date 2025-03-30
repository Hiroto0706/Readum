class ResultGetBaseException(Exception):
    """クイズ取得に関連する基底例外クラス"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResultNotFoundError(ResultGetBaseException):
    """クイズ結果が取得できなかった場合のエラー"""

    pass


class GetResultObjectError(ResultGetBaseException):
    """オブジェクト取得処理中に発生したエラー"""

    pass
