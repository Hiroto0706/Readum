import logging
import os
import uuid
from fastapi import APIRouter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_community.vectorstores import FAISS
from langsmith import Client
from src.infrastructure.database_file_handler import DBFileHandlerImpl
from src.infrastructure.vectordb import VectorStoreHandlerImpl
from src.infrastructure.doc_creator import DocumentCreatorImpl
from config.settings import Settings
from src.infrastructure.rag_agent import RAGAgentModelImpl
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
    text_splitter = CharacterTextSplitter(
        chunk_size=Settings.text_splitter.CHUNK_SIZE,
        chunk_overlap=Settings.text_splitter.CHUNK_OVERLAP,
    )

    if quiz_request.type == QuizType.TEXT:
        document_creator = DocumentCreatorImpl(_text_splitter=text_splitter)
        document = document_creator.translate_str_into_doc(quiz_request.content)
    elif quiz_request.type == QuizType.URL:
        document_loader = FireCrawlLoader(
            url=quiz_request.content, mode="scrape", params={"onlyMainContent": True}
        )
        document_creator = DocumentCreatorImpl(document_loader, text_splitter)
        document = document_creator.load_document()

    # ベクトルDBにドキュメントを保存する
    splitted_doc = document_creator.split_document(document)
    embeddings = OpenAIEmbeddings(model=Settings.model.TEXT_EMBEDDINGS_MODEL)
    vector_store_handler = VectorStoreHandlerImpl(
        embeddings, FAISS.from_documents(splitted_doc, embeddings)
    )

    db_file_handler = DBFileHandlerImpl()
    directory_path = db_file_handler.create_unique_directory()

    # ベクトルDBにデータを保存
    vector_store_handler.save_local(directory_path)

    client = Client(api_key=Settings.lang_chain.LANGCHAIN_API_KEY)
    prompt = client.pull_prompt("readum-system-prompt")
    llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL)
    rag_agent = RAGAgentModelImpl(llm, prompt)

    rag_agent = rag_agent.set_rag_chain(
        vector_store_handler.as_retriever(directory_path)
    )
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    # プロンプトテンプレートを作成

    try:
        res = rag_agent.invoke_chain(
            question_count=quiz_request.question_count,
            difficulty=quiz_request.difficulty.value,
        )
        return QuizResponse(id=db_file_handler.get_unique_id(), preview=res)
    finally:
        db_file_handler.delete_unique_directory()

    # TODO: 例外処理やエラーハンドリングを実装する


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
