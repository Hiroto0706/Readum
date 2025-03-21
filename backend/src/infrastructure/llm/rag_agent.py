import logging
from operator import itemgetter
from typing import Any
from pydantic.dataclasses import dataclass

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI

from src.domain.entities.quiz import Quiz
from src.domain.service.rag_agent import RAGAgentModel


logger = logging.getLogger(__name__)


@dataclass(frozen=True, config=dict(arbitrary_types_allowed=True))
class RAGAgentModelImpl(RAGAgentModel):
    """RAG Agentを実装し、クイズを生成するモデル"""

    _llm: ChatOpenAI
    _prompt: Any
    _rag_chain: Any

    def set_rag_chain(self, retriever: VectorStoreRetriever) -> "RAGAgentModel":
        """RAGを実行するためのChainを生成する"""
        rag_chain = (
            {
                "question_count": itemgetter("question_count"),
                "difficulty": itemgetter("difficulty"),
                "input": itemgetter("input"),
                "context": itemgetter("input") | retriever,
            }
            | self._prompt
            | self._llm.with_structured_output(Quiz)
        )
        return RAGAgentModelImpl(self._llm, self._prompt, rag_chain)

    def invoke_chain(self, question_count: int, difficulty: str) -> "Quiz":
        """RAG Chainの実装"""
        try:
            response = self._rag_chain.invoke(
                {
                    # FIXME: 一旦inputは固定値としておく
                    "input": "Please generate the quiz according to the above instructions.",
                    "question_count": question_count,
                    "difficulty": difficulty,
                }
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error(
                f"Error while invoking RAG Chain with question_count={question_count} and difficulty={question_count}: {e}",
                exc_info=True,
            )
