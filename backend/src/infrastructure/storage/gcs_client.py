import json
import logging
from google.cloud import storage

from src.domain.entities.results import UserAnswer

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

    # TODO: 引数の型定義を行う
    def save_quiz_submission(self, quiz_id: str, submission_data: UserAnswer):
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
