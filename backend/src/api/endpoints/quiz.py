import logging
from fastapi import APIRouter, Depends

from src.application.usecase.quiz_creator import QuizCreator
from src.api.models.quiz import QuizResponse, QuizRequest


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/create_quiz", response_model=QuizResponse)
async def create_quiz(quiz_request: QuizRequest, quiz_creator=Depends(QuizCreator())):
    """
    ユーザーが入力した条件をもとにクイズを生成する。

    Args:
        type (QuizType): 入力タイプ（テキストorURL）
        content (str): 読書メモまたはURL
        difficulty (Difficulty): クイズの難易度
        question_count (int): クイズの数

    Returns:
        QuizResponse: クイズのリスト（選択肢、解答、解説）
    """
    res: QuizResponse = quiz_creator.create_quiz(
        quiz_request.type,
        quiz_request.content,
        quiz_request.question_count,
        quiz_request.difficulty,
    )
    return res


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
