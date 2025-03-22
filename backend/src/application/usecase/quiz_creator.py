from pydantic.dataclasses import dataclass

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_community.vectorstores import FAISS
from langsmith import Client

from src.api.models.quiz import Difficulty, QuizResponse, QuizType
from src.infrastructure.llm.rag_agent import RAGAgentModelImpl
from src.infrastructure.db.vectordb import VectorStoreHandlerImpl
from src.infrastructure.file_system.database_file_handler import DBFileHandlerImpl
from src.infrastructure.llm.doc_creator import DocumentCreatorImpl

from config.settings import Settings


@dataclass(frozen=True)
class QuizCreator:
    def create_quiz(
        quiz_type: QuizType, content: str, question_count: int, difficulty: Difficulty
    ) -> QuizResponse:
        """
        基本的にクイズを生成するフローをここで管理することにする。

        1. 入力を受け取り、テキストスプリットを行う
        →URLの時はFireCrawlを使ってスクレイピングを行う

        2. ベクトルDBに埋め込む

        3. RAG Chainを作成する

        4. Chainの実行
        """

        text_splitter = CharacterTextSplitter(
            chunk_size=Settings.text_splitter.CHUNK_SIZE,
            chunk_overlap=Settings.text_splitter.CHUNK_OVERLAP,
        )

        if quiz_type == QuizType.TEXT:
            document_creator = DocumentCreatorImpl(text_splitter=text_splitter)
            document = document_creator.translate_str_into_doc(content)
        elif quiz_type == QuizType.URL:
            document_loader = FireCrawlLoader(
                url=content,
                mode="scrape",
                params={"onlyMainContent": True},
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
        try:
            directory_path = db_file_handler.create_unique_directory()
            vector_store_handler.save_local(directory_path)

            client = Client(api_key=Settings.lang_chain.LANGCHAIN_API_KEY)
            prompt = client.pull_prompt("readum-system-prompt")
            llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL)
            rag_agent = RAGAgentModelImpl(llm, prompt)

            rag_agent = rag_agent.set_rag_chain(
                vector_store_handler.as_retriever(directory_path)
            )

            res = rag_agent.invoke_chain(
                question_count=question_count,
                difficulty=difficulty.value,
            )
            return QuizResponse(id=db_file_handler.get_unique_id(), preview=res)
        finally:
            db_file_handler.delete_unique_directory()
