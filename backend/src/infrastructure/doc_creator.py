import logging
from typing import List
from pydantic import Field
from pydantic.dataclasses import dataclass
from langchain_text_splitters.base import TextSplitter
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from src.domain.repositories.doc_creator_repository import DocumentCreator


logger = logging.getLevelName(__name__)


@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class DocumentCreatorImpl(DocumentCreator):
    """ドキュメントの生成を行うクラスの抽象クラス"""

    _document_loader: BaseLoader = Field(
        default=None, description="ドキュメントロードインスタンス"
    )
    _text_splitter: TextSplitter = Field(
        ..., description="テキストスプリッターインスタンス"
    )

    def translate_str_into_doc(self, text: str) -> List[Document]:
        """str型の文字列をDocument型に変換する関数"""
        texts = self._text_splitter.split_text(text)
        documents = [
            Document(page_content=txt, metadata={"source": "text"}) for txt in texts
        ]
        return documents

    def load_document(self) -> List[Document]:
        """対象のドキュメントを読み込む関数"""
        try:
            documents = self._document_loader.load()
        except Exception as e:
            logger.error(logger.error(f"Failed to load document : {e}", exc_info=True))
            raise RuntimeError(f"Failed to load document.") from e
        return documents

    def split_document(self, document: List[Document]) -> List[Document]:
        """受け取ったドキュメントを分割する関数"""
        splitted_document = self._text_splitter.split_documents(document)
        return splitted_document
