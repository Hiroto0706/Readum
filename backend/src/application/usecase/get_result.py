import logging
from pydantic import BaseModel, ConfigDict

from src.domain.entities.results import UserAnswer
from src.application.exceptions.get_result_exceptions import (
    GetResultObjectError,
    ResultNotFoundError,
)
from src.infrastructure.storage.gcs_client import GCSClient


logger = logging.getLogger(__name__)


class ResultGetter(BaseModel):
    """
    ユーザーの回答結果を取得するモデル
    """

    quiz_id: str
    storage_client: GCSClient

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, quiz_id: str):

        storage_client = GCSClient()
        super().__init__(quiz_id=quiz_id, storage_client=storage_client)

    def get_result_object_from_storage(self) -> UserAnswer:
        try:
            res = self.storage_client.get_result(self.quiz_id)

            if not res:
                error_msg = f"Result with UUID {self.quiz_id} not found"
                raise ResultNotFoundError(error_msg)

            return res
        except Exception as e:
            error_msg = f"Failed to get object from storage: {str(e)}"
            logger.error(error_msg)
            raise GetResultObjectError(error_msg)
