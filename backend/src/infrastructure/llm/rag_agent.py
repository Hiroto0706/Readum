import logging
import json
from operator import itemgetter
from typing import Any

from langchain_core.tools import tool
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

from src.domain.entities.quiz import Quiz
from src.domain.service.rag_agent import RAGAgentModel
from src.infrastructure.exceptions.llm_exceptions import (
    LLMResponseParsingError,
    RAGChainExecutionError,
    RAGChainSetupError,
)


logger = logging.getLogger(__name__)


class RAGAgentModelImpl(RAGAgentModel):
    """RAG Agentを実装し、クイズを生成するモデル"""

    def __init__(
        self, llm: BaseChatModel, prompt: Any, retriever: VectorStoreRetriever
    ):
        super().__init__(llm=llm, prompt=prompt)
        # rag を実行するchainの作成
        self.rag_chain = self._set_rag_chain(retriever=retriever)

        # create_graph()の中でToolsからtoolを取得し、グラフを生成する
        self.graph = self._create_graph()

    def _create_chain(self, retriever: VectorStoreRetriever) -> Runnable:
        """RAGを実行するためのChainを生成する"""
        rag_chain = (
            {
                "question_count": itemgetter("question_count"),
                "difficulty": itemgetter("difficulty"),
                "input": itemgetter("input"),
                "context": itemgetter("input") | retriever,
            }
            | self.prompt
            | self.llm.with_structured_output(Quiz)
        )
        return rag_chain

    def _set_rag_chain(self, retriever: VectorStoreRetriever) -> Runnable:
        """RAGを実行するためのChainをクラスに設定する"""
        try:
            rag_chain = self._create_chain(retriever)
            return rag_chain

        except Exception as e:
            error_msg = f"Failed to set up RAG chain: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RAGChainSetupError(error_msg)

    def invoke_chain(self, question_count: int, difficulty: str) -> "Quiz":
        """RAG Chainの実装"""
        if not self.rag_chain:
            error_msg = "RAG chain is not initialized. Call set_rag_chain first."
            logger.error(error_msg)
            raise RAGChainExecutionError(error_msg)

        try:
            response = self.rag_chain.invoke(
                {
                    "input": f"Generate {question_count} quiz questions of difficulty '{difficulty}'.",
                    "question_count": question_count,
                    "difficulty": difficulty,
                }
            )
            logger.info(response)
            return response

        except ValueError as e:
            error_msg = f"Failed to parse LLM response: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise LLMResponseParsingError(error_msg)

        except Exception as e:
            error_msg = f"Error while invoking RAG Chain with question_count={question_count} and difficulty={difficulty}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RAGChainExecutionError(error_msg)
