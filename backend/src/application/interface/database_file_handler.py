import uuid
from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict, Field


class DBFileHandler(ABC, BaseModel, frozen=True):
    """DBのインデックスのファイル操作を行うモデルの規定クラス"""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    def _create_unique_dir_path(self, unique_id: str):
        """ファイル保存先のディレクトリのパスを生成する"""
        pass

    @abstractmethod
    def create_unique_directory(self, unique_id: str) -> str:
        """target_pathにDBファイル保存用のディレクトリを構築する"""
        pass

    @abstractmethod
    def delete_unique_directory(self, unique_id: str):
        """target_pathのディレクトリを削除する関数"""
        pass
