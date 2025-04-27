import logging
from operator import itemgetter
from typing import Any, Dict

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

    def _create_graph(self):
        """LangGraphを用いてAIエージェントを構築する"""
        try:
            logger.info("Creating LangGraph with Supervisor architecture")

            @tool
            def generate_quiz_tool(
                question_count: int,
                difficulty: str,
                instruction: str | None = None,
            ) -> Quiz | None:
                """
                文脈を取得し、クイズを生成するツール
                1. retrieverで文脈を取得
                2. 文脈が短すぎるとNoneを返す
                3. RAG Chainを呼び出し、Quizを生成する
                """
                quiz_input = {
                    "input": instruction
                    or f"Generate {question_count} quiz questions of difficulty '{difficulty}'.",
                    "question_count": question_count,
                    "difficulty": difficulty,
                }
                logger.debug(f"Invoking chain with parameters: {quiz_input}")

                try:
                    result = self.rag_chain.invoke(quiz_input)
                    logger.debug(
                        f"Generated quiz with {len(result.questions)} questions"
                    )
                    return result
                except Exception as e:
                    logger.error(f"Error Generating quiz: {str(e)}")
                    return None

            @tool
            def refine_instruction_tool(
                quiz: Quiz | None,
                issues: list[str] = [],  # consistency_check → issues に変更
            ) -> str:
                """
                問題数や一貫性の問題がある場合の再生成指示文を返すツール
                """
                if quiz is None:
                    return "The context is insufficient to generate a quiz. Please provide more relevant information."

                if not issues:  # 問題リストが空の場合
                    return "The quiz looks good."

                instruction = (
                    "Please regenerate the quiz with the following corrections:\n"
                )
                instruction += "\n".join(f"- {issue}" for issue in issues)

                logger.debug(f"Refinement instruction: {instruction}")
                return instruction

            # RAGエージェント定義
            logger.info("Creating RAG quiz agent")
            self.rag_agent = create_react_agent(
                model=self.llm,
                tools=[generate_quiz_tool],
                name="rag_quiz_agent",
                prompt=(
                    "You are RAGQuizAgent. "
                    "Generate a quiz based on the stored context using "
                    "generate_quiz_tool(question_count, difficulty, instruction). "
                    "Return None if context is insufficient."
                ),
            )

            # 評価エージェント定義 - ツールを使わず評価させる
            logger.info("Creating evaluation agent")
            self.evaluate_agent = create_react_agent(
                model=self.llm,
                tools=[refine_instruction_tool],
                name="evaluate_agent",
                prompt=(
                    "You are EvaluateAgent that reviews quizzes. Your task is to analyze a quiz and identify any issues.\n\n"
                    "Review Process:\n"
                    "1. Check if the quiz has EXACTLY the specified number of questions. The quiz MUST have exactly the number requested.\n"
                    "2. Verify each question has a valid answer (must be one of: A, B, C, or D).\n"
                    "3. Ensure the explanation for each question correctly matches and explains the chosen answer.\n"
                    "4. Check for any inconsistencies between questions, answers, and explanations.\n\n"
                    "If you find ANY issues, create a list of specific problems and use refine_instruction_tool(quiz, question_count, issues) "
                    "to generate instructions for refinement. Be thorough and specific about what needs to be fixed.\n\n"
                    "If no issues are found, use refine_instruction_tool(quiz, question_count) without an issues list."
                ),
            )

            # Supervisor定義
            logger.info("Creating supervisor agent")
            supervisor = create_supervisor(
                agents=[self.rag_agent, self.evaluate_agent],
                model=self.llm,
                prompt=(
                    "You are a supervisor for quiz generation. "
                    "Loop between rag_quiz_agent and evaluate_agent up to 5 times. "
                    "If generate_quiz_tool returns None at any point, "
                    "return None to indicate insufficient context. "
                    "Your goal is to produce a high-quality quiz with the correct number of questions, "
                    "where answers and explanations are consistent."
                ),
            )

            # グラフをコンパイル
            graph = supervisor.compile()
            logger.info("LangGraph successfully created and compiled")
            return graph

        except Exception as e:
            error_msg = f"Failed to create LangGraph: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RAGChainSetupError(error_msg)

    def graph_run(
        self,
        question_count: int,
        difficulty: str,
    ) -> Quiz:
        """LangGraphを用いてクイズを生成する"""
        try:
            result = self.graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "question_count": question_count,
                                "difficulty": difficulty,
                            },
                        }
                    ]
                }
            )

            logger.info(
                f"Successfully generated quiz with {len(result.questions)} questions via LangGraph"
            )
            return result

        except ValueError as e:
            error_msg = f"Failed to parse LLM response: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise LLMResponseParsingError(error_msg)

        except Exception as e:
            error_msg = f"Error while running LangGraph: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RAGChainExecutionError(error_msg)
