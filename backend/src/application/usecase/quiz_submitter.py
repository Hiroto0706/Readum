import logging
from typing import Optional

from pydantic import BaseModel

from src.application.exceptions.quiz_submit_exception import (
    SaveObjectToStorageError,
)
from src.infrastructure.storage.gcs_client import GCSClient
from src.api.models.quiz import UserAnswer


logger = logging.getLogger(__name__)


class QuizSubmitter(BaseModel):
    user_answer: UserAnswer
    storage_client: Optional[GCSClient] = None

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, user_answer: UserAnswer):
        """
        Storageにユーザーの回答を含むクイズオブジェクトを保存する。

        Args:
          user_answer: UserAnswer
        """
        super().__init__(user_answer=user_answer)

        bucket_name = "quiz_answer"
        self.storage_client = GCSClient(bucket_name)

    def save_object_to_storage(self):
        """
        Storageにuser_answerを保存する。
        """
        # TODO: clientの保存関数を叩く
        quiz_id = self.user_answer.id
        try:
            user_answer_dict = self.user_answer.model_dump()
            self.storage_client.save_quiz_submission(quiz_id, user_answer_dict)
        except Exception as e:
            error_msg = f"Failed to save object to storage: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise SaveObjectToStorageError(error_msg) from e
