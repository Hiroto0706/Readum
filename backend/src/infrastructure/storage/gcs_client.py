import json
import logging
from typing import Any
from google.cloud import storage

from config.settings import Settings


logger = logging.getLogger(__name__)


class GCSClient:
    def __init__(self):
        """
        Google Cloud Storageクライアントを初期化します。

        Args:
            bucket_name (str): 保存先のバケット名
        """
        self.storage_client = storage.Client()

        self.bucket_name = "readum"
        env = Settings.app.ENV
        self.prefix = f"{env}/results/"

        # バケットが存在するか確認し、なければ作成
        try:
            self.bucket = self.storage_client.get_bucket(self.bucket_name)
        except Exception:
            logger.info(f"Bucket {self.bucket_name} does not exist. Creating...")
            self.bucket = self.storage_client.create_bucket(self.bucket_name)

    def save_quiz_submission(self, quiz_id: str, submission_data: Any):
        """
        クイズの回答をGCSに保存します。

        Args:
            quiz_id (str): クイズのID
            submission_data (dict): 保存するデータ

        Returns:
            str: 保存したファイルのパス
        """
        try:
            blob_name = f"{self.prefix}{quiz_id}.json"
            blob = self.bucket.blob(blob_name)

            # データをJSON形式で保存
            blob.upload_from_string(
                json.dumps(submission_data, ensure_ascii=False, indent=2),
                content_type="application/json",
            )

            logger.info(f"Saved quiz submission to gs://{self.bucket_name}/{blob_name}")
            return blob_name

        except Exception as e:
            logger.error(f"Error saving quiz object to GCS: {str(e)}")
            raise

    def get_result(self, quiz_id: str) -> Any:
        """
        uuidをもとにCloud Storageからユーザーの回答を取得する

        Args:
          uuid(str): uuid

        Returns:
          TODO: あとで書く
        """
        try:
            blob_name = f"{self.prefix}{quiz_id}.json"
            blob = self.bucket.blob(blob_name)

            if not blob:
                logger.warning(f"No submission found for quiz_id: {quiz_id}")
                return None

            content = blob.download_as_text()
            submission_data = json.loads(content)

            logger.info(f"Retrieved quiz submission from {blob_name}")
            return submission_data

        except Exception as e:
            logger.error(f"Failed to retrieve quiz submission: {str(e)}")
            raise
