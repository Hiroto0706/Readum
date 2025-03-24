import logging
from operator import itemgetter
from typing import Any
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI

from src.domain.entities.quiz import Quiz
from src.domain.service.rag_agent import RAGAgentModel
from src.infrastructure.exceptions.llm_exceptions import (
    LLMResponseParsingError,
    RAGChainExecutionError,
    RAGChainSetupError,
)


logger = logging.getLogger(__name__)


@dataclass(frozen=True, config=ConfigDict(arbitrary_types_allowed=True))
class RAGAgentModelImpl(RAGAgentModel):
    """RAG Agentを実装し、クイズを生成するモデル"""

    llm: ChatOpenAI
    prompt: Any
    rag_chain: Any

    def set_rag_chain(self, retriever: VectorStoreRetriever) -> "RAGAgentModel":
        """RAGを実行するためのChainを生成する"""
        try:
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
            return RAGAgentModelImpl(self.llm, self.prompt, rag_chain)

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
                    # FIXME: 一旦inputは固定値としておく
                    "input": "Please generate the quiz according to the above instructions.",
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
