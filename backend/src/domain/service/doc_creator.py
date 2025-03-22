from abc import ABC, abstractmethod
from typing import List
from pydantic import Field
from pydantic.dataclasses import dataclass

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters.base import TextSplitter


@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class DocumentCreator(ABC):
    """ドキュメントの生成を行うクラスの抽象クラス"""

    _document_loader: BaseLoader = Field(
        default=None, description="ドキュメントロードインスタンス"
    )
    _text_splitter: TextSplitter = Field(
        ..., description="テキストスプリッターインスタンス"
    )

    @abstractmethod
    def translate_str_into_doc(self, text: str) -> List[Document]:
        """str型の文字列をDocument型に変換する関数"""
        pass

    @abstractmethod
    def load_document(self) -> List[Document]:
        """対象のドキュメントを読み込む関数"""
        pass

    @abstractmethod
    def split_document(self, document: List[Document]) -> List[Document]:
        """受け取ったドキュメントを分割する関数"""
        pass
