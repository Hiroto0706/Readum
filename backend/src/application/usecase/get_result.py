from typing import Optional
from pydantic import BaseModel

from src.application.exceptions.get_result_exceptions import ResultNotFoundError
from src.infrastructure.storage.gcs_client import GCSClient


class ResultGetter(BaseModel):
    """
    ユーザーの回答結果を取得するモデル
    """

    quiz_id: str
    storage_client: Optional[GCSClient] = None

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, quiz_id: str):
        super().__init__(quiz_id=quiz_id)

        bucket_name = "quiz_answer"
        self.storage_client = GCSClient(bucket_name)

    def get_result_object_from_storage(self):
        res = self.storage_client.get_result(self.quiz_id)

        if not res:
            error_msg = f"Result with UUID {self.quiz_id} not found"
            raise ResultNotFoundError(error_msg)

        return res
