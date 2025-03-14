import logging
import os
import uuid
import shutil
from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_text_splitters import CharacterTextSplitter

from config.settings import Settings
from src.api.models.request import QuizRequest, QuizType
from src.api.models.response import QuizResponse

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

    # UUIDを生成して、TMPディレクトリ内にユニークなサブディレクトリを作成する
    unique_id = uuid.uuid4().hex

    logger.info(unique_id)

    unique_dir = os.path.join(Settings.embeddings.TMP_VECTORDB_PATH, unique_id)

    logger.info(unique_dir)

    os.makedirs(unique_dir, exist_ok=True)

    vectorstore.save_local(unique_dir)
    new_vectorstore = FAISS.load_local(
        unique_dir,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = new_vectorstore.as_retriever(search_kwargs={"k": 8})

    prompt_template = """
    以下の文脈だけを踏まえて質問に答えてください。

    コンテクスト:
    {context}

    タスク：{question}
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL).with_structured_output(
        QuizResponse
    )

    rag_chain = {"question": RunnablePassthrough(), "context": retriever} | prompt | llm
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    # プロンプトテンプレートを作成

    question = f"""
    コンテクスト情報を元に、読書メモの理解度チェックのためのクイズを{quiz_request.question_count}問作成してください。

    クイズは{quiz_request.difficulty.value}の難易度で作成してください。
    クイズの難易度は全部で3つあります。
    1. beginner: 初学者向けのクイズ
    2. intermediate: 中級者向けのクイズ
    3. advanced: 上級者向けのクイズ

    クイズはA~Dの4択にしてください。
    回答は詳細に記載してください。
    クイズの内容はコンテキストに基づいたものにしてください。
    読書の目的といった主観的な内容はクイズにしないでください。客観的な事実だけクイズにしてください。
    感想をクイズにするのではなく、コンテキストの内容を踏まえたクイズを作成してください。
    """

    try:
        res = rag_chain.invoke(question)
        print(res)

        quiz_response = res
    finally:
        shutil.rmtree(unique_dir)

    # TODO: 例外処理やエラーハンドリングを実装する

    return quiz_response


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
