import logging
import os
import shutil

from src.infrastructure.exceptions.file_system_exceptions import (
    DirectoryCreationError,
    DirectoryDeletionError,
)
from src.application.interface.database_file_handler import (
    DBFileHandler,
)

from config.settings import Settings

logger = logging.getLogger(__name__)


class DBFileHandlerImpl(DBFileHandler):
    """DBのインデックスのファイル操作を行うモデルの規定クラス"""

    def _create_unique_dir_path(self, unique_id: str):
        """ファイル保存先のディレクトリのパスを生成する"""
        return os.path.join(
            Settings.embeddings.TMP_VECTORDB_PATH,
            Settings.embeddings.VECTORDB_PROVIDER,
            unique_id,
        )

    def create_unique_directory(self, unique_id: str) -> str:
        """target_pathにDBファイル保存用のディレクトリを構築する"""
        try:
            dir_path = self._create_unique_dir_path(unique_id)
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

    def delete_unique_directory(self, unique_id: str):
        """target_pathのディレクトリを削除する関数"""
        try:
            dir_path = self._create_unique_dir_path(unique_id)
            shutil.rmtree(dir_path)

        except FileNotFoundError as e:
            logger.warn(f"The target directory '{dir_path}' was not found: {e}")

        except Exception as e:
            error_msg = f"Failed to delete directory: {dir_path}. Error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DirectoryDeletionError(error_msg)
