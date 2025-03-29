import logging
from typing import List
from pydantic import Field

from langchain_text_splitters import CharacterTextSplitter, TextSplitter
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from src.domain.service.doc_creator import DocumentCreator
from src.infrastructure.exceptions.llm_exceptions import (
    DocumentLoadError,
    DocumentSplitException,
)

from config.settings import Settings


logger = logging.getLogger(__name__)


class DocumentLoaderImpl(DocumentCreator):
    """ドキュメントの読み込みを行うクラスの抽象クラス"""

    document_loader: BaseLoader = Field(
        ..., description="ドキュメントロードインスタンス"
    )
    text_splitter: TextSplitter = Field(
        default_factory=lambda: CharacterTextSplitter(
            chunk_size=Settings.text_splitter.CHUNK_SIZE,
            chunk_overlap=Settings.text_splitter.CHUNK_OVERLAP,
        ),
        description="テキストスプリッターインスタンス",
    )

    def load_document(self) -> List[Document]:
        """対象のドキュメントを読み込む関数"""
        try:
            documents = self.document_loader.load()
            return documents
        except Exception as e:
            error_msg = f"Failed to load document: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DocumentLoadError(error_msg)

    def split_document(self, document: List[Document]) -> List[Document]:
        """受け取ったドキュメントを分割する関数"""
        if not document:
            logger.warning("Empty document list provided for splitting")
            return []

        try:
            splitted_document = self.text_splitter.split_documents(document)

            return splitted_document
        except ValueError as e:
            error_msg = f"Invalid document format for splitting: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DocumentSplitException(error_msg)
        except Exception as e:
            error_msg = f"Failed to split document: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise DocumentSplitException(error_msg)
