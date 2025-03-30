import logging

from pydantic import BaseModel, ConfigDict

from src.application.exceptions.quiz_submit_exceptions import (
    SaveObjectToStorageError,
)
from src.infrastructure.storage.gcs_client import GCSClient
from src.api.models.quiz import UserAnswer


logger = logging.getLogger(__name__)


class QuizSubmitter(BaseModel):
    user_answer: UserAnswer
    storage_client: GCSClient

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, user_answer: UserAnswer):
        """
        Storageにユーザーの回答を含むクイズオブジェクトを保存する。

        Args:
          user_answer: UserAnswer
        """

        storage_client = GCSClient()
        super().__init__(user_answer=user_answer, storage_client=storage_client)

    def save_object_to_storage(self):
        """
        Storageにuser_answerを保存する。
        """
        # TODO: clientの保存関数を叩く
        quiz_id = self.user_answer.id
        try:
            user_answer_dict = self.user_answer.model_dump()
            self.storage_client.save_quiz(quiz_id, user_answer_dict)
        except Exception as e:
            error_msg = f"Failed to save object to storage: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise SaveObjectToStorageError(error_msg) from e
