from abc import ABC, abstractmethod
from typing import Final, List
from pydantic import BaseModel, ConfigDict, Field

from langchain_core.documents import Document
from langchain_text_splitters.base import TextSplitter


class DocumentCreator(ABC, BaseModel):
    """ドキュメントの生成を行うクラスの抽象クラス"""

    text_splitter: TextSplitter = Field(
        ..., description="テキストスプリッターインスタンス"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    def split_document(self, document: List[Document]) -> List[Document]:
        """受け取ったドキュメントを分割する関数"""
        pass
