import logging
import os
import shutil
import uuid
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from src.infrastructure.exceptions.file_system_exceptions import (
    DirectoryCreationError,
    DirectoryDeletionError,
)
from src.application.interface.database_file_handler import (
    DBFileHandler,
)

from config.settings import Settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True, config=ConfigDict(arbitrary_types_allowed=True))
class DBFileHandlerImpl(DBFileHandler):
    """DBのインデックスのファイル操作を行うモデルの規定クラス"""

    unique_id: str = uuid.uuid4().hex

    def get_unique_id(self) -> str:
        return super().get_unique_id()

    def _create_unique_dir_path(self):
        """ファイル保存先のディレクトリのパスを生成する"""
        return os.path.join(
            Settings.embeddings.TMP_VECTORDB_PATH,
            Settings.embeddings.VECTORDB_PROVIDER,
            self.unique_id,
        )

    def create_unique_directory(self) -> str:
        """target_pathにDBファイル保存用のディレクトリを構築する"""
        try:
            dir_path = self._create_unique_dir_path()
            os.makedirs(dir_path, exist_ok=True)

            logger.info(f"Created directory in a {dir_path}.")

            return dir_path

        except FileNotFoundError as e:
            error_msg = (
                f"Parent directory path does not exist for: {dir_path}. Error: {str(e)}"
            )
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        except Exception as e:
            error_msg = f"An unexpected error occurred while creating directory: {dir_path}. Error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DirectoryCreationError(error_msg)

    def delete_unique_directory(self):
        """target_pathのディレクトリを削除する関数"""
        try:
            dir_path = self._create_unique_dir_path()
            shutil.rmtree(dir_path)

        except FileNotFoundError as e:
            logger.warn(f"The target directory '{dir_path}' was not found: {e}")

        except Exception as e:
            error_msg = f"Failed to delete directory: {dir_path}. Error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DirectoryDeletionError(error_msg)
