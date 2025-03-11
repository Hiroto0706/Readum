import logging
from fastapi import APIRouter


from src.api.models.request import QuizRequest
from src.api.models.response import Quiz, QuizOption, QuizPreview, QuizResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


router = APIRouter()


@router.post("/create_quiz", response_model=QuizResponse)
async def create_quiz(question_base: QuizRequest):
    """
    ユーザーが入力した条件をもとにクイズを生成する。

    Args:
        type (str): 入力タイプ（テキストorURL）
        content (str): 読書メモまたはURL
        difficulty (str): クイズの難易度
        question_count (int): クイズの数

    Returns:
        QuizResponse: クイズのリスト（選択肢、解答、解説）
    """
    # TODO: 入力内容の前処理（テキストのクリーニング、チャンク化など）を実施する

    # TODO: 前処理済みテキストからFAISS用のベクトル埋め込みを生成する（Hugging Faceの埋め込み等を使用）

    # TODO: FAISS検索を利用して、関連するチャンクを取得する

    # TODO: RAG（Retrieval-Augmented Generation）パイプラインを実装し、LLMを呼び出してテスト問題を生成する

    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する

    quiz_response = QuizResponse(
        preview=QuizPreview(
            questions=[
                Quiz(
                    content="この物語の主人公は誰ですか？",
                    options=QuizOption(
                        A="アリス",
                        B="ボブ",
                        C="チャーリー",
                        D="ダイアン",
                    ),
                    answer="A",
                    explanation="物語の冒頭で主人公として描かれているのはアリスです。",
                ),
                Quiz(
                    content="次のうち、著者の主張に最も近いものはどれですか？",
                    options=QuizOption(
                        A="技術革新は経済成長の鍵である。",
                        B="伝統は未来を切り開く。",
                        C="教育は社会を変革する。",
                        D="自然との共生が最重要である。",
                    ),
                    answer="C",
                    explanation="本文では、教育の持つ変革力に焦点が当てられています。",
                ),
                Quiz(
                    content="この文章で筆者が最も強調している点は何ですか？",
                    options=QuizOption(
                        A="革新的なアイデアの重要性",
                        B="リスク管理の方法",
                        C="持続可能な開発",
                        D="グローバル化の影響",
                    ),
                    answer="C",
                    explanation="持続可能な開発が筆者の主張の中心にあるためです。",
                ),
            ]
        )
    )

    # TODO: 例外処理やエラーハンドリングを実装する

    return quiz_response


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
