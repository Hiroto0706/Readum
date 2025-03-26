from pydantic.dataclasses import dataclass


@dataclass
class QuizSubmitBaseException(Exception):
  """クイズの保存に関連する基底例外クラス"""

  message: str

  def __post_init__(self):
    super().__init__(self.message)


@dataclass
class SaveObjectToStorageError(QuizSubmitBaseException):
  """Storageにオブジェクトを保存する処理中のエラー"""
  pass