import logging
from uuid import UUID
from fastapi import APIRouter

from src.api.exceptions.quiz_exceptions import handle_application_exception
from src.application.usecase.get_result import ResultGetter


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{uuid}")
async def get_result(uuid: str):
    """
    UUIDをもとにユーザーの回答を取得する

    Args:
        uuid: UUID

    Returns:
        UserAnswer: ユーザーの回答結果
    """
    try:
        # TODO: 環境変数で管理しよう
        result_getter = ResultGetter(uuid)
        res = result_getter.get_result_object_from_storage()

        return res

    except Exception as e:
        logger.error(f"Error creating quiz: {str(e)}", exc_info=True)
        raise handle_application_exception(e)
