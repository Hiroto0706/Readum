import logging
from uuid import UUID
from fastapi import APIRouter


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


router = APIRouter()


@router.post("/create_question")
async def create_question():
    """
    Create questions from input content.
    """
    # TODO: リクエストからユーザーの入力内容（読書メモやURLなど）を抽出・検証する
    # TODO: 入力内容の前処理（テキストのクリーニング、チャンク化など）を実施する
    # TODO: 前処理済みテキストからFAISS用のベクトル埋め込みを生成する（Hugging Faceの埋め込み等を使用）
    # TODO: FAISS検索を利用して、関連するチャンクを取得する
    # TODO: RAG（Retrieval-Augmented Generation）パイプラインを実装し、LLMを呼び出してテスト問題を生成する
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    # TODO: ユーザーに返却するレスポンス形式（問題文、選択肢、正解、解説など）を構築する
    # TODO: 例外処理やエラーハンドリングを実装する
    return {"message": "Hello, World from FastAPI"}


@router.post("/correction")
async def correction():
    """
    Correction user's answer
    """
    pass


@router.get("/result/{uuid}")
async def get_result(uuid: UUID):
    """
    Get user's test result
    """
    pass
