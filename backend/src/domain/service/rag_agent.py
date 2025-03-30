from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever

from src.domain.entities.quiz import Quiz


class RAGAgentModel(BaseModel, ABC):
    """RAGを実装実装し、クイズを生成するための抽象モデル"""

    llm: BaseChatModel = Field(..., description="LLMモデル")
    prompt: Any = Field(..., description="プロンプトテンプレート")
    rag_chain: Any = Field(default=None, description="RAG Chain", init=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def set_rag_chain(self, retriever: VectorStoreRetriever) -> "RAGAgentModel":
        """RAGを実行するためのChainを生成する"""
        pass

    @abstractmethod
    def invoke_chain(self, query: str, question_count: int, difficulty: str) -> "Quiz":
        """RAG Chainの実行"""
        pass
