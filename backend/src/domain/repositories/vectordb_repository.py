from abc import ABC, abstractmethod
from typing import Final
from pydantic import Field

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever


class VectorStoreHandler(ABC):
    embeddings_model: Final[Embeddings] = Field(..., description="埋め込みモデル")
    vectorstore: Final[VectorStore] = Field(
        default=None, description="ベクトルストアインスタンス"
    )

    @abstractmethod
    def set_vectorstore(self) -> "VectorStoreHandler":
        """ベクトルストアをセットする"""
        pass

    @abstractmethod
    def save_local(self, dir_path: str) -> None:
        """
        ベクトルストアのデータを指定されたディレクトリに保存します。
        """
        pass

    @abstractmethod
    def as_retriever(self, dir_path: str) -> VectorStoreRetriever:
        """
        ベクトルストアからリトリーバー（検索機能）を返します。
        """
        pass
