import uuid
from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass


@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class DBFileHandler(ABC):
    """DBのインデックスのファイル操作を行うモデルの規定クラス"""

    _unique_id: str = uuid.uuid4().hex

    @abstractmethod
    def get_unique_id(self) -> str:
        return self._unique_id

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
