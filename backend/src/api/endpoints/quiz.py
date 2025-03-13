import logging
from fastapi import APIRouter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub

from config.settings import Settings
from src.api.models.request import QuizRequest, QuizType
from src.api.models.response import Quiz, QuizOption, QuizPreview, QuizResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


router = APIRouter()


@router.post("/create_quiz", response_model=QuizResponse)
async def create_quiz(quiz_request: QuizRequest):
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
    embeddings = OpenAIEmbeddings()

    if quiz_request.type == QuizType.TEXT:
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        texts = text_splitter.split_text(quiz_request.content)

        # ベクトルストア作成
        vectorstore = FAISS.from_texts(texts, embeddings)
    elif quiz_request.type == QuizType.URL:
        loader = FireCrawlLoader(
            url=quiz_request.content, mode="scrape", params={"onlyMainContent": True}
        )
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        documents = text_splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(documents, embeddings)

    vectorstore.save_local(Settings.embeddings.TMP_VECTORDB_PATH)
    new_vectorstore = FAISS.load_local(
        Settings.embeddings.TMP_VECTORDB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    new_vectorstore.as_retriever().search_kwargs["k"] = 5

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        ChatOpenAI(model_name=Settings.model.GPT_MODEL), retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_docs_chain
    )
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    res = retrieval_chain.invoke(
        {"input": "理解度チェックのためのクイズを選択形式で10問生成してください。"}
    )
    print(res)

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
