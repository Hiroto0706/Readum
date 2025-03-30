import json
import logging
from typing import Any, Dict
from google.cloud import storage

from src.domain.repositories.storage_repository import StorageService
from src.domain.entities.results import UserAnswer

from config.settings import Settings


logger = logging.getLogger(__name__)


class GCSClient(StorageService):
    storage_client: storage.Client
    bucket_name: str
    prefix: str
    bucket: storage.Bucket

    def __init__(self):
        """
        Google Cloud Storageクライアントを初期化します。

        Args:
            bucket_name (str): 保存先のバケット名
        """
        storage_client = storage.Client()
        bucket_name = "readum"
        env = Settings.app.ENV
        prefix = f"{env}/results/"

        # バケットが存在するか確認し、なければ作成
        try:
            bucket = storage_client.get_bucket(bucket_name)
        except Exception:
            logger.info(f"Bucket {bucket_name} does not exist. Creating...")
            bucket = storage_client.create_bucket(bucket_name)

        super().__init__(
            storage_client=storage_client,
            bucket_name=bucket_name,
            prefix=prefix,
            bucket=bucket,
        )

    def save_quiz(self, quiz_id: str, data_dict: Dict[str, Any]) -> str:
        """
        クイズの回答をGCSに保存し、保存先のパスを返す

        Args:
            quiz_id (str): クイズのID
            data_dict (Dict[str, Any]): 保存するデータ

        Returns:
            str: 保存したファイルのパス
        """
        try:
            blob_name = f"{self.prefix}{quiz_id}.json"
            blob = self.bucket.blob(blob_name)

            # データをJSON形式で保存
            blob.upload_from_string(
                json.dumps(data_dict, ensure_ascii=False, indent=2),
                content_type="application/json",
            )

            logger.info(f"Saved quiz submission to gs://{self.bucket_name}/{blob_name}")
            return blob_name

        except Exception as e:
            logger.error(f"Error saving quiz object to GCS: {str(e)}")
            raise

    def get_result(self, quiz_id: str) -> UserAnswer | None:
        """
        uuidをもとにCloud Storageからユーザーの回答を取得する

        Args:
          quiz_id(str): クイズのID

        Returns:
          UserAnswer: UserAnswer型のデータ。見つからない場合はNone
        """
        try:
            blob_name = f"{self.prefix}{quiz_id}.json"
            blob = self.bucket.blob(blob_name)

            if not blob.exists():
                logger.warning(f"No submission found for quiz_id: {quiz_id}")
                return None

            content = blob.download_as_text()
            submission_data = json.loads(content)

            logger.info(f"Retrieved quiz submission from {blob_name}")
            return submission_data

        except Exception as e:
            logger.error(f"Failed to retrieve quiz submission: {str(e)}")
            raise
