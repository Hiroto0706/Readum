import logging
from operator import itemgetter
import os
import uuid
import shutil
from fastapi import APIRouter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langsmith import Client

from config.settings import Settings
from src.infrastructure.embeddings.embeddings import EmbeddingsModelImpl
from src.api.models.request import QuizRequest, QuizType
from src.api.models.response import QuizResponse

logger = logging.getLogger(__name__)


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
    embeddings = OpenAIEmbeddings(model=Settings.model.TEXT_EMBEDDINGS_MODEL)
    text_splitter = CharacterTextSplitter(
        chunk_size=Settings.text_splitter.CHUNK_SIZE,
        chunk_overlap=Settings.text_splitter.CHUNK_OVERLAP,
    )

    embeddings_model = EmbeddingsModelImpl(
        _model=embeddings, _text_splitter=text_splitter
    )

    if quiz_request.type == QuizType.TEXT:
        doc_text = embeddings_model.text_to_doc(quiz_request.content)
        splitted_doc = embeddings_model.text_split(doc_text)
    elif quiz_request.type == QuizType.URL:
        url: str = quiz_request.content
        embeddings_model = embeddings_model.set_document_loader(url)
        documents = embeddings_model.load_document()
        splitted_doc = embeddings_model.text_split(documents)

    embeddings_model = embeddings_model.set_vectorstore(splitted_doc)

    # UUIDを生成して、TMPディレクトリ内にユニークなサブディレクトリを作成する
    unique_id = uuid.uuid4().hex

    logger.info(unique_id)

    unique_dir = os.path.join(
        Settings.embeddings.TMP_VECTORDB_PATH,
        Settings.embeddings.VECTORDB_PROVIDER,
        unique_id,
    )

    logger.info(unique_dir)

    os.makedirs(unique_dir, exist_ok=True)

    embeddings_model.save_inmemory(unique_dir)

    new_vectorstore = FAISS.load_local(
        unique_dir,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    retriever = new_vectorstore.as_retriever(search_kwargs={"k": 8})

    client = Client(api_key=Settings.lang_chain.LANGCHAIN_API_KEY)
    prompt = client.pull_prompt("readum-system-prompt")

    llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL).with_structured_output(
        QuizResponse
    )

    rag_chain = (
        {
            "question_count": itemgetter("question_count"),
            "difficulty": itemgetter("difficulty"),
            "input": itemgetter("input"),
            "context": itemgetter("input") | retriever,
        }
        | prompt
        | llm
    )
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    # プロンプトテンプレートを作成

    try:
        res = rag_chain.invoke(
            {
                "input": "Please generate the quiz according to the above instructions.",
                "question_count": quiz_request.question_count,
                "difficulty": quiz_request.difficulty.value,
            }
        )
        logger.info(res)

        quiz_response = res
    finally:
        embeddings_model.cleanup(unique_dir)

    # TODO: 例外処理やエラーハンドリングを実装する

    return quiz_response


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
