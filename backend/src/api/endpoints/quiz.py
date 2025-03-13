import logging
from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

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

    vectorstore.save_local(Settings.embeddings.TMP_VECTORDB_PATH)
    new_vectorstore = FAISS.load_local(
        Settings.embeddings.TMP_VECTORDB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    retriever = new_vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt_template = """
    以下のコンテクスト情報を元に、読書メモの理解度チェックのためのクイズを{question_count}問作成してください。
    クイズは{difficulty}の難易度で作成してください。
    クイズはA~Dの4択にしてください。

    コンテクスト:
    {context}
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL, temperature=0)
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        ChatOpenAI(model_name="gpt-4o-2024-05-13"), retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_docs_chain
    )

    rag_chain = (
        {
            "context": retrieval_chain | retriever.map(),
            "question_count": lambda _: quiz_request.question_count,
            "difficulty": lambda _: quiz_request.difficulty,
        }
        | prompt
        | llm.with_structured_output(QuizResponse)
    )
    # TODO: Pydanticなどを利用して、生成されたテスト問題をパース・検証する
    # プロンプトテンプレートを作成

    res = rag_chain.invoke({})
    print(res)

    quiz_response = res

    # TODO: 例外処理やエラーハンドリングを実装する

    return quiz_response


@router.post("/correct")
async def correction():
    """
    Correction user's answer
    """
    pass
