import json
import logging
from typing import Any
from google.cloud import storage

from config.settings import Settings


logger = logging.getLogger(__name__)


class GCSClient:
    def __init__(self, bucket_name="quiz_answers"):
        """
        Google Cloud Storageクライアントを初期化します。

        Args:
            bucket_name (str): 保存先のバケット名
        """
        self.storage_client = storage.Client()

        env = Settings.app.ENV
        self.bucket_name = f"readum/{env}/results"

        # バケットが存在するか確認し、なければ作成
        try:
            self.bucket = self.storage_client.get_bucket(bucket_name)
        except Exception:
            logger.info(f"Bucket {bucket_name} does not exist. Creating...")
            self.bucket = self.storage_client.create_bucket(bucket_name)

    def save_quiz_submission(self, quiz_id: str, submission_data: Any):
        """
        クイズの回答をGCSに保存します。

        Args:
            quiz_id (str): クイズのID
            submission_data (dict): 保存するデータ

        Returns:
            str: 保存したファイルのパス
        """
        blob_name = f"{quiz_id}.json"
        blob = self.bucket.blob(blob_name)

        # データをJSON形式で保存
        blob.upload_from_string(
            json.dumps(submission_data, ensure_ascii=False, indent=2),
            content_type="application/json",
        )

        logger.info(f"Saved quiz submission to gs://{self.bucket_name}/{blob_name}")
        return blob_name

    def get_result(self, quiz_id: str):
        """
        uuidをもとにCloud Storageからユーザーの回答を取得する

        Args:
          uuid(str): uuid

        Returns:
          TODO: あとで書く
        """
        try:
            blobs = list(self.bucket.list_blobs(prefix=quiz_id))

            if not blobs:
                logger.warning(f"No submission found for quiz_id: {quiz_id}")
                return None

            latest_blob = sorted(blobs, key=lambda x: x.name, reverse=True)[0]

            content = latest_blob.download_as_text()

            submission_data = json.loads(content)

            logger.info(f"Retrieved quiz submission from {latest_blob.name}")
            return submission_data

        except Exception as e:
            logger.error(f"Failed to retrieve quiz submission: {str(e)}")
            raise
