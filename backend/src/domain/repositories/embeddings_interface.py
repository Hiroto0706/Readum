from abc import ABC, abstractmethod
from typing import List
from langchain_text_splitters.base import TextSplitter
from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass
from langchain_core.embeddings import Embeddings
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore


@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class EmbeddingsModel(ABC):
    """ベクトルDBへの埋め込みを行う抽象モデル"""

    _model: Embeddings = Field(..., description="埋め込みモデル")
    _text_splitter: TextSplitter = Field(
        ..., description="テキストスプリッターインスタンス"
    )
    _document_loader: BaseLoader = Field(
        default=None, description="ドキュメントロードインスタンス"
    )
    _vectorstore: VectorStore = Field(
        default=None, description="ベクトルストアインスタンス"
    )

    @abstractmethod
    def text_to_doc(self, content: str) -> List[Document]:
        """str型の文字列をDocument型に変換する関数"""
        pass

    @abstractmethod
    def set_document_loader(self, url: str) -> "EmbeddingsModel":
        """DocumentLoaderのインスタンスを返す関数"""
        pass

    @abstractmethod
    def load_document(self) -> List[Document]:
        """対象のドキュメントを読み込む関数"""
        pass

    @abstractmethod
    def text_split(self, document: List[Document]) -> List[Document]:
        """受け取ったテキストを分割する関数"""
        pass

    @abstractmethod
    def set_vectorstore(self, document: List[Document]) -> "EmbeddingsModel":
        """ベクトルストアを作成する関数"""
        pass

    @abstractmethod
    def save_inmemory(self, target_path: str) -> None:
        """インメモリのベクトルストアにベクトルデータを保存する"""
        pass

    @abstractmethod
    def cleanup(self, target_path: str) -> None:
        """インメモリをクリーンアップする関数"""
        pass
