import logging
from typing import List, Tuple
import uuid
from pydantic import BaseModel

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders.firecrawl import FireCrawlLoader

from src.infrastructure.llm.doc_translate import DocumentTranslateImpl
from src.domain.repositories.vectordb_repository import VectorStoreHandler
from src.application.interface.database_file_handler import DBFileHandler
from src.api.models.quiz import Difficulty, QuizResponse, QuizType
from src.application.exceptions.quiz_creation_exceptions import (
    DocumentProcessingError,
    InsufficientContextError,
    InvalidInputError,
    RAGProcessingError,
    VectorStoreOperationError,
)
from src.application.service.llm_service import get_prompt_from_hub
from src.infrastructure.llm.rag_agent import RAGAgentModelImpl
from src.infrastructure.db.vectordb import VectorStoreHandlerImpl, get_faiss_index
from src.infrastructure.file_system.database_file_handler import DBFileHandlerImpl
from src.infrastructure.llm.doc_loader import DocumentLoaderImpl
from src.infrastructure.exceptions.vectordb_exceptions import (
    VectorStoreCreationError,
    VectorStoreSaveError,
    VectorStoreLoadError,
    InvalidDocumentError,
)
from src.infrastructure.exceptions.llm_exceptions import (
    LLMResponseParsingError,
    RAGChainExecutionError,
    RAGChainSetupError,
)
from src.infrastructure.exceptions.file_system_exceptions import (
    DirectoryCreationError,
    DirectoryDeletionError,
)

from config.settings import settings


logger = logging.getLogger(__name__)


# TODO: 初期値としてquizという値を受け取るようにする
class QuizCreator(BaseModel):
    def create_quiz(
        self,
        quiz_type: QuizType,
        content: str,
        question_count: int,
        difficulty: Difficulty,
    ) -> QuizResponse:
        """
        クイズを生成する関数

        Args:
            quiz_type: クイズの種類（テキストまたはURL）
            content: クイズの元となるコンテンツ（テキストまたはURL）
            question_count: 生成する問題数
            difficulty: 難易度

        Returns:
            生成されたクイズのレスポンス

        Raises:
            InvalidInputError: 入力パラメータが無効な場合
            DocumentProcessingError: ドキュメント処理中にエラーが発生した場合
            VectorStoreOperationError: ベクトルストア操作中にエラーが発生した場合
            RAGProcessingError: RAG処理中にエラーが発生した場合
        """
        # FIXME: API層でバリデーションは行ってもいいかも
        if not content:
            error_msg = "Content cannot be empty"
            logger.error(error_msg)
            raise InvalidInputError(error_msg)

        if quiz_type == QuizType.TEXT and len(content) < 100:
            error_msg = "TEXT type content must be at least 100 characters long."
            logger.error(error_msg)
            raise InvalidInputError(error_msg)

        if question_count <= 0:
            error_msg = (
                f"Invalid question_count: {question_count}. Must be greater than 0."
            )
            logger.error(error_msg)
            raise InvalidInputError(error_msg)

        uuid = self._generate_uuid()

        db_file_handler = DBFileHandlerImpl()
        directory_path = None

        try:
            # ドキュメント処理
            try:
                splitted_doc = self._process_document(quiz_type, content)
            except Exception as e:
                error_msg = f"Failed to process document: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise DocumentProcessingError(error_msg) from e

            # ベクトルストア操作
            try:
                vector_store_handler, directory_path = self._setup_vector_store(
                    splitted_doc, db_file_handler, uuid
                )
            except (
                VectorStoreCreationError,
                VectorStoreSaveError,
                InvalidDocumentError,
                DirectoryCreationError,
            ) as e:
                error_msg = f"Vector store operation failed: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise VectorStoreOperationError(error_msg) from e
            except Exception as e:
                error_msg = f"Unexpected error during vector store operation: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise VectorStoreOperationError(error_msg) from e

            # RAG処理
            try:
                return self._process_rag(
                    vector_store_handler,
                    directory_path,
                    question_count,
                    difficulty,
                    uuid,
                )
            except (
                RAGChainSetupError,
                RAGChainExecutionError,
                LLMResponseParsingError,
                VectorStoreLoadError,
            ) as e:
                error_msg = f"RAG processing failed: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise RAGProcessingError(error_msg) from e
            except Exception as e:
                error_msg = f"Unexpected error during RAG processing: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise RAGProcessingError(error_msg) from e

        finally:
            # リソース解放
            self._cleanup_resources(directory_path, db_file_handler, uuid)

    def _process_document(self, quiz_type: QuizType, content: str) -> List[Document]:
        """ドキュメント処理を行うヘルパーメソッド"""

        if quiz_type == QuizType.TEXT:
            document_translator = DocumentTranslateImpl()
            document = document_translator.translate_str_into_doc(content)
            splitted_doc = document_translator.split_document(document)
        elif quiz_type == QuizType.URL:
            document_loader = FireCrawlLoader(
                url=content,
                mode="scrape",
                params={"onlyMainContent": True},
            )
            document_loader = DocumentLoaderImpl(document_loader=document_loader)
            document = document_loader.load_document()
            splitted_doc = document_loader.split_document(document)

        return splitted_doc

    def _setup_vector_store(
        self, splitted_doc: List[Document], db_file_handler: DBFileHandler, uuid: str
    ) -> Tuple[VectorStoreHandler, str]:
        """ベクトルストアのセットアップを行うヘルパーメソッド"""
        embeddings = OpenAIEmbeddings(model=settings.model.TEXT_EMBEDDINGS_MODEL)
        vector_store_handler = VectorStoreHandlerImpl(
            embeddings_model=embeddings,
            vectorstore=get_faiss_index(splitted_doc, embeddings),
        )

        directory_path = db_file_handler.create_unique_directory(uuid)
        vector_store_handler.save_local(directory_path)

        return vector_store_handler, directory_path

    def _process_rag(
        self,
        vector_store_handler: VectorStoreHandler,
        directory_path: str,
        question_count: int,
        difficulty: QuizType,
        uuid: str,
    ) -> QuizResponse:
        """RAG処理を行うヘルパーメソッド"""
        prompt = get_prompt_from_hub()
        llm = ChatOpenAI(model_name=settings.model.GPT_MODEL)
        retriever = vector_store_handler.as_retriever(directory_path)
        rag_agent = RAGAgentModelImpl(llm=llm, prompt=prompt, retriever=retriever)

        # if settings.app.USE_LANGGRAPH:
        rag_response = rag_agent.graph_run(
            question_count=question_count,
            difficulty=difficulty.value,
        )
        # else:
        #     rag_response = rag_agent.invoke_chain(
        #         question_count=question_count,
        #         difficulty=difficulty.value,
        #     )

        if rag_response is None:
            logger.warning("Graph run returned None")
            raise InsufficientContextError("Insufficient context to generate a quiz")

        return QuizResponse(
            id=uuid, preview=rag_response, difficulty_value=difficulty.value
        )

    def _cleanup_resources(
        self, directory_path: str, db_file_handler: DBFileHandler, uuid: str
    ) -> None:
        """リソース解放を行うヘルパーメソッド"""
        if directory_path:
            try:
                db_file_handler.delete_unique_directory(uuid)
            except DirectoryDeletionError as e:
                logger.warning(f"Failed to clean up directory: {str(e)}")
            except Exception as e:
                logger.warning(f"Unexpected error during cleanup: {str(e)}")
        else:
            logger.error("directory_path is empty or None, cannot perform cleanup")

    @staticmethod
    def _generate_uuid() -> str:
        return uuid.uuid4().hex
