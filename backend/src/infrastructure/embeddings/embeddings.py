import logging
import shutil
from sys import exc_info
from typing import List
from urllib.parse import urlparse
from langchain_core.document_loaders import BaseLoader
from langchain_openai import OpenAIEmbeddings
from pydantic.dataclasses import dataclass
from langchain_text_splitters.base import TextSplitter
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from src.domain.repositories.embeddings_interface import EmbeddingsModel
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

logger = logging.getLevelName(__name__)


# FIXME: 範囲が狭いので一つのクラスで実装しているが、要件が大きくなれば細かく責任を分ける必要尾あり
@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class EmbeddingsModelImpl(EmbeddingsModel):
    """ベクトルDBへの埋め込みを行うモデル"""

    _model: OpenAIEmbeddings
    _text_splitter: TextSplitter
    _document_loader: None | FireCrawlLoader
    _vectorstore: None | FAISS

    def text_to_doc(self, content: str) -> List[Document]:
        texts = self._text_splitter.split_text(content)
        documents = [
            Document(page_content=txt, metadata={"source": "text"}) for txt in texts
        ]
        return documents

    @staticmethod
    def _check_url(url: str) -> None:
        """入力がURL形式かどうかチェックする"""
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            logger.info("The entered value is not in URL format.")
            raise ValueError(
                "When the 'type' field is set to 'url', the 'content' field must be in a valid URL format."
            )

    def set_document_loader(self, url: str) -> "EmbeddingsModelImpl":
        # urlがURL形式かどうかチェック
        self._check_url(url)

        document_loader = FireCrawlLoader(
            url=url, mode="scrape", params={"onlyMainContent": True}
        )

        # この時点ではvectorstoreは存在しないため代入しないï
        return EmbeddingsModelImpl(
            _model=self._model,
            _text_splitter=self._text_splitter,
            _document_loader=document_loader,
        )

    def load_document(self) -> List[Document]:
        """入力がURLの場合、FireCrawlを使用してドキュメントを取得する"""

        try:
            documents = self._document_loader.load()
        except Exception as e:
            logger.error(logger.error(f"Failed to load document : {e}", exc_info=True))
            raise RuntimeError(f"Failed to load document.") from e
        return documents

    def text_split(self, document: List[Document]) -> List[Document]:
        """入力されたドキュメントを分割する関数"""
        splitted_document = self._text_splitter.split_documents(document)
        return splitted_document

    def set_vectorstore(self, documents: List[Document]) -> "EmbeddingsModelImpl":
        """FAISSインデックスを作成する関数"""
        embeddings = self._model
        new_vectorstore = FAISS.from_documents(documents, embeddings)

        return EmbeddingsModelImpl(
            _model=self._model,
            _text_splitter=self._text_splitter,
            _document_loader=self._document_loader,
            _vectorstore=new_vectorstore,
        )

    def save_inmemory(self, target_path: str) -> None:
        """FAISSインデックスにベクトルデータを保存する関数"""
        if not self._vectorstore:
            logger.warn("vectorstore instance is not defined.")
            return

        try:
            self._vectorstore.save_local(target_path)
        except Exception as e:
            logger.error(
                f"Failed to save vectorstore to {target_path}: {e}", exc_info=True
            )
            raise RuntimeError(
                f"An error occurred while saving the vectorstore to {target_path}."
            ) from e

    def cleanup(self, target_path: str) -> None:
        """target_path配下のFAISSインデックスを削除する"""
        try:
            shutil.rmtree(target_path)
        except FileNotFoundError as e:
            logger.warn(
                f"The target directory '{target_path}' was not found: {e}",
                exc_info=True,
            )
        except Exception as e:
            logger.error(
                f"Failed to cleanup vectorstore at '{target_path}': {e}", exc_info=True
            )
            raise RuntimeError(f"Failed to cleanup vectorstore at {target_path}") from e
