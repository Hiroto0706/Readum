import logging
from typing import List
from pydantic import Field

from langchain_text_splitters import CharacterTextSplitter, TextSplitter
from langchain_core.documents import Document

from src.domain.service.doc_creator import DocumentCreator
from src.infrastructure.exceptions.llm_exceptions import (
    DocumentSplitException,
    TranslationError,
)

from config.settings import settings


logger = logging.getLogger(__name__)


class DocumentTranslateImpl(DocumentCreator):
    """ドキュメントの翻訳を行うクラスの抽象クラス"""

    text_splitter: TextSplitter = Field(
        default_factory=lambda: CharacterTextSplitter(
            chunk_size=settings.text_splitter.CHUNK_SIZE,
            chunk_overlap=settings.text_splitter.CHUNK_OVERLAP,
        ),
        description="テキストスプリッターインスタンス",
    )

    def translate_str_into_doc(self, text: str) -> List[Document]:
        """str型の文字列をDocument型に変換する関数"""
        try:
            texts = self.text_splitter.split_text(text)
            documents = [
                Document(page_content=txt, metadata={"source": "text"}) for txt in texts
            ]
            return documents
        except Exception as e:
            error_msg = f"Failed to translate string to document: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise TranslationError(error_msg)

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
