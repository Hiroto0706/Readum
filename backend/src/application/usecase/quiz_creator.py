import logging
from pydantic.dataclasses import dataclass

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_community.vectorstores import FAISS

from src.api.models.quiz import Difficulty, QuizResponse, QuizType
from src.application.exceptions.quiz_creation_exceptions import (
    DocumentProcessingError,
    InvalidInputError,
    RAGProcessingError,
    VectorStoreOperationError,
)
from src.application.service.llm_service import get_prompt_from_hub
from src.infrastructure.llm.rag_agent import RAGAgentModelImpl
from src.infrastructure.db.vectordb import VectorStoreHandlerImpl
from src.infrastructure.file_system.database_file_handler import DBFileHandlerImpl
from src.infrastructure.llm.doc_creator import DocumentCreatorImpl
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

        if question_count <= 0:
            error_msg = (
                f"Invalid question_count: {question_count}. Must be greater than 0."
            )
            logger.error(error_msg)
            raise InvalidInputError(error_msg)

        db_file_handler = DBFileHandlerImpl()
        directory_path = None

        try:
            try:
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

            except Exception as e:
                error_msg = f"Failed to process document: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise DocumentProcessingError(error_msg)

            try:
                embeddings = OpenAIEmbeddings(
                    model=Settings.model.TEXT_EMBEDDINGS_MODEL
                )
                vector_store_handler = VectorStoreHandlerImpl(
                    embeddings_model=embeddings,
                    vectorstore=FAISS.from_documents(splitted_doc, embeddings),
                )

                directory_path = db_file_handler.create_unique_directory()
                vector_store_handler.save_local(directory_path)

            except (
                VectorStoreCreationError,
                VectorStoreSaveError,
                InvalidDocumentError,
                DirectoryCreationError,
            ) as e:
                error_msg = f"Vector store operation failed: {str(e)}"
                logger.error(error_msg)
                raise VectorStoreOperationError(error_msg)

            except Exception as e:
                error_msg = f"Unexpected error during vector store operation: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise VectorStoreOperationError(error_msg)

            try:
                prompt = get_prompt_from_hub()
                llm = ChatOpenAI(model_name=Settings.model.GPT_MODEL)
                rag_agent = RAGAgentModelImpl(llm=llm, prompt=prompt, _rag_chain=None)

                retriever = vector_store_handler.as_retriever(directory_path)
                rag_agent = rag_agent.set_rag_chain(retriever)

                rag_response = rag_agent.invoke_chain(
                    question_count=question_count,
                    difficulty=difficulty.value,
                )

                return QuizResponse(
                    id=db_file_handler.get_unique_id(), preview=rag_response
                )

            except (
                RAGChainSetupError,
                RAGChainExecutionError,
                LLMResponseParsingError,
                VectorStoreLoadError,
            ) as e:
                error_msg = f"RAG processing failed: {str(e)}"
                logger.error(error_msg)
                raise RAGProcessingError(error_msg)

            except Exception as e:
                error_msg = f"Unexpected error during RAG processing: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise RAGProcessingError(error_msg)

        finally:
            if directory_path:
                try:
                    db_file_handler.delete_unique_directory()
                except DirectoryDeletionError as e:
                    logger.warning(f"Failed to clean up directory: {str(e)}")
                except Exception as e:
                    logger.warning(f"Unexpected error during cleanup: {str(e)}")
