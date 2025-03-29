import uuid
from abc import ABC, abstractmethod

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


def generate_uuid() -> str:
    return uuid.uuid4().hex


@dataclass(frozen=True, config=ConfigDict(arbitrary_types_allowed=True))
class DBFileHandler(ABC):
    """DBのインデックスのファイル操作を行うモデルの規定クラス"""

    unique_id: str = Field(default_factory=generate_uuid)

    @abstractmethod
    def get_unique_id(self) -> str:
        return self.unique_id

    @abstractmethod
    def _create_unique_dir_path(unique_id: str):
        """ファイル保存先のディレクトリのパスを生成する"""
        pass

    @abstractmethod
    def create_unique_directory(self) -> str:
        """target_pathにDBファイル保存用のディレクトリを構築する"""
        pass

    @abstractmethod
    def delete_unique_directory(self):
        """target_pathのディレクトリを削除する関数"""
        pass
