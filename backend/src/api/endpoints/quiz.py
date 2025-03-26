import logging
from fastapi import APIRouter

from src.api.exceptions.quiz_exceptions import handle_application_exception
from src.application.usecase.quiz_creator import QuizCreator
from src.api.models.quiz import QuizResponse, QuizRequest, UserAnswer


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/create_quiz", response_model=QuizResponse)
async def create_quiz(quiz_request: QuizRequest):
    """
    ユーザーが入力した条件をもとにクイズを生成する。

    Args:
        type (QuizType): 入力タイプ（テキストorURL）
        content (str): 読書メモまたはURL
        difficulty (Difficulty): クイズの難易度
        question_count (int): クイズの数

    Returns:
        QuizResponse: クイズのリスト（選択肢、解答、解説）

    Raises:
        BadRequestError: 入力されたパラメータ処理中にエラーが発生した場合（404）
        InternalServerError: ドキュメント、ベクトルデータベース、RAGの処理中にエラーが発生した場合（500）
    """
    try:
        quiz_creator = QuizCreator()
        res: QuizResponse = quiz_creator.create_quiz(
            quiz_request.type,
            quiz_request.content,
            quiz_request.question_count,
            quiz_request.difficulty,
        )
        return res

    except ValueError as e:
        logger.error(f"Invalid input value: {str(e)}", exc_info=True)
        raise handle_application_exception(e)

    except Exception as e:
        logger.error(f"Error creating quiz: {str(e)}", exc_info=True)
        raise handle_application_exception(e)


@router.post("/submit")
async def submit_answer(user_answer: UserAnswer):
    """
    ユーザーの回答内容をGCSに保存する。

    Args:
        type (QuizType): 入力タイプ（テキストorURL）
        content (str): 読書メモまたはURL
        difficulty (Difficulty): クイズの難易度
        question_count (int): クイズの数
    """
    pass
