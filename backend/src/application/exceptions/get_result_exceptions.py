from pydantic.dataclasses import dataclass


@dataclass
class ResultGetBaseException(Exception):
    """クイズ取得に関連する基底例外クラス"""

    message: str

    def __post_init__(self):
        super().__init__(self.message)


@dataclass
class ResultNotFoundError(ResultGetBaseException):
    """クイズ結果が取得できなかった場合のエラー"""

    pass


@dataclass
class GetResultObjectError(ResultGetBaseException):
    """オブジェクト取得処理中に発生したエラー"""

    pass
