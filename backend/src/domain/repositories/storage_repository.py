from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict

from src.domain.entities.results import UserAnswer


class StorageService(ABC, BaseModel):
    """ストレージを操作するためのハンドラークラス"""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    def save_quiz(self, quiz_id: str, data_dict: Dict[str, Any]) -> str:
        """
        クイズの回答をGCSに保存し、保存先のパスを返す

        Args:
            quiz_id (str): クイズのID
            data_dict (Dict[str, Any]): 保存するデータ

        Returns:
            str: 保存したファイルのパス
        """
        pass

    @abstractmethod
    def get_result(self, quiz_id: str) -> UserAnswer | None:
        """
        uuidをもとにCloud Storageからユーザーの回答を取得する

        Args:
          quiz_id(str): クイズのID

        Returns:
          UserAnswer: UserAnswer型のデータ。見つからない場合はNone
        """
        pass
