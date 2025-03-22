from pydantic.dataclasses import dataclass
import logging
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from src.domain.repositories.vectordb_repository import VectorStoreHandler


logger = logging.getLevelName(__name__)


@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class VectorStoreHandlerImpl(VectorStoreHandler):
    """
    FAISSインデックスを操作するために必要なメソッドの実態をここで定義する
    """

    _embeddings_model: OpenAIEmbeddings
    _vectorstore: None | FAISS

    def set_vectorstore(self, document: List[Document]) -> "VectorStoreHandlerImpl":
        vectorstore = FAISS.from_documents(document, self._embeddings_model)

        return VectorStoreHandlerImpl(
            _embeddings_model=self._embeddings_model,
            _vectorstore=vectorstore,
        )

    def save_local(self, dir_path: str) -> None:
        """
        ベクトルストアのデータを指定されたディレクトリに保存します。
        """
        if not self._vectorstore:
            logger.warn("vectorstore instance is not defined.")
            return

        try:
            self._vectorstore.save_local(dir_path)
        except Exception as e:
            logger.error(f"Failed to save vectorstore to {dir_path}: {e}")
            raise RuntimeError(
                f"An error occurred while saving the vectorstore to {dir_path}."
            ) from e

    def as_retriever(self, dir_path: str) -> VectorStoreRetriever:
        """
        ベクトルストアからリトリーバー（検索機能）を返します。
        """
        vectorstore = FAISS.load_local(
            dir_path, self._embeddings_model, allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
        return retriever
