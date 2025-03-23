import logging
from pydantic.dataclasses import dataclass

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_community.vectorstores import FAISS

from src.api.models.quiz import Difficulty, QuizResponse, QuizType
from src.application.service.llm_service import get_prompt_from_hub
from src.infrastructure.llm.rag_agent import RAGAgentModelImpl
from src.infrastructure.db.vectordb import VectorStoreHandlerImpl
from src.infrastructure.file_system.database_file_handler import DBFileHandlerImpl
from src.infrastructure.llm.doc_creator import DocumentCreatorImpl

from config.settings import Settings


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class QuizCreator:
    def create_quiz(
        self,
        quiz_type: QuizType,
        content: str,
        question_count: int,
        difficulty: Difficulty,
    ) -> QuizResponse:
        """
        クイズを生成する関数
        """
        if quiz_type == QuizType.TEXT:
            document_creator = DocumentCreatorImpl()
            document = document_creator.translate_str_into_doc(content)
        elif quiz_type == QuizType.URL:
            document_loader = FireCrawlLoader(
                url=content,
                mode="scrape",
                params={"onlyMainContent": True},
            )
            document_creator = DocumentCreatorImpl(document_loader)
            document = document_creator.load_document()

        splitted_doc = document_creator.split_document(document)
        embeddings = OpenAIEmbeddings(model=Settings.model.TEXT_EMBEDDINGS_MODEL)
        vector_store_handler = VectorStoreHandlerImpl(
            embeddings, FAISS.from_documents(splitted_doc, embeddings)
        )

        db_file_handler = DBFileHandlerImpl()
        try:
            directory_path = db_file_handler.create_unique_directory()
            vector_store_handler.save_local(directory_path)

            prompt = get_prompt_from_hub()
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
        except Exception as e:
            logger.error(f"予期せぬエラーが発生しました: {e}")
            raise
        finally:
            db_file_handler.delete_unique_directory()
