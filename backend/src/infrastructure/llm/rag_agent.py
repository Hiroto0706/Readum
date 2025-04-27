import logging
import json
import re
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
            def output_schema():
                """
                QuizおよびQuestionの構造化データスキーマを返す

                クイズ生成時に使用する標準的なデータ構造を定義します。
                このスキーマに厳密に従うことで、一貫性のあるクイズ生成が可能になります。

                構造:
                    questions (list[Question]): クイズの質問リスト
                        Question:
                            content (str): 質問文のテキスト（例:「人生において最も重要な資本は何か？」）
                            options (dict): キーA,B,C,Dと対応する選択肢のテキストからなる辞書
                                A (str): 選択肢A（例:「金融資本」）
                                B (str): 選択肢B（例:「人的資本」）
                                C (str): 選択肢C（例:「社会資本」）
                                D (str): 選択肢D（例:「時間資本」）
                            answer (str): 正解の選択肢のキー（例:「B」）
                            explanation (str): 正解の理由と他の選択肢が不正解である理由の説明

                Example:
                    {
                        "questions": [
                            {
                                "content": "人生において最も重要な資本は何か？",
                                "options": {
                                    "A": "金融資本",
                                    "B": "人的資本",
                                    "C": "社会資本",
                                    "D": "時間資本"
                                },
                                "answer": "B",
                                "explanation": "本文では人的資本が最も重要であると述べられています。金融資本は人的資本の結果として得られるものであり、社会資本は人的資本を基盤として構築されます。時間資本という概念は本文には登場しません。"
                            }
                        ]
                    }

                注意:
                    - キー 'questions' を必ず使用してください（'quiz' ではありません）
                    - 各質問には 'content' キーを使用してください（'question' ではありません）
                    - 'options' は配列ではなく辞書形式にしてください
                    - 'answer' は有効な選択肢（A, B, C, D）のいずれかである必要があります
                """
                schema = """
                {
                    "questions": [
                        {
                            "content": "質問文",
                            "options": {
                                "A": "選択肢A",
                                "B": "選択肢B",
                                "C": "選択肢C",
                                "D": "選択肢D"
                            },
                            "answer": "A",
                            "explanation": "解説文"
                        }
                    ]
                }
                """
                return schema

            # RAGエージェント定義
            logger.info("Creating RAG quiz agent")
            self.rag_agent = create_react_agent(
                model=self.llm,
                tools=[generate_quiz_tool, output_schema],
                name="rag_quiz_agent",
                prompt=(
                    "You are RAGQuizAgent. "
                    "Generate a quiz based on the stored context using "
                    "generate_quiz_tool(question_count, difficulty, instruction). "
                    "Return None if context is insufficient. "
                    "Use output_schema() to ensure your result follows the required format. "
                    "YOUR FINAL OUTPUT MUST CONFORM TO THE SCHEMA PROVIDED BY OUTPUT_SCHEMA TOOL."
                ),
            )

            # 評価エージェント定義
            logger.info("Creating evaluation agent")
            self.evaluate_agent = create_react_agent(
                model=self.llm,
                tools=[],
                name="evaluate_agent",
                prompt=(
                    "You are EvaluateAgent that reviews quizzes. Your task is to analyze a quiz and identify any issues.\n\n"
                    "Review Process:\n"
                    "1. Check if the quiz has EXACTLY the specified number of questions.\n"
                    "2. Verify each question has a valid answer (must be one of: A, B, C, or D).\n"
                    "3. Ensure the explanation for each question correctly matches the chosen answer.\n"
                    "4. Check for any inconsistencies or errors in the content.\n\n"
                    "If issues are found, explain them in detail. If no issues are found, simply state 'The quiz looks good.'\n"
                    "Your role is to provide feedback - you don't need to directly modify the quiz."
                ),
            )

            # Supervisor定義
            logger.info("Creating supervisor agent")
            supervisor = create_supervisor(
                agents=[self.rag_agent, self.evaluate_agent],
                model=self.llm,
                prompt=(
                    "You are RAGQuizAgent. Follow these steps STRICTLY IN THIS ORDER: "
                    "1. FIRST, generate a quiz based on the stored context using generate_quiz_tool(question_count, difficulty, instruction). "
                    "2. SECOND, you MUST evaluate the generated quiz using evaluate_agent to check if the questions are appropriate, accurate, and well-formed. "
                    "3. THIRD, if the evaluation suggests improvements OR if the number of questions does not match the requested amount, ALWAYS have the rag_quiz_agent generate a revised quiz. "
                    "4. FOURTH, repeat steps 2-3 until the quiz meets all requirements including the correct number of questions. "
                    "THIS WORKFLOW IS MANDATORY - DO NOT SKIP ANY STEP OR IGNORE EVALUATION FEEDBACK! "
                    "IF CONTEXT IS INSUFFICIENT OR GENERATE_QUIZ_TOOL RETURNS NONE, YOU MUST RETURN ONLY THE STRING 'None' WITHOUT ANY ADDITIONAL TEXT OR FORMATTING. "
                    "You MUST use output_schema() tool to understand the required format. "
                    "YOUR FINAL OUTPUT MUST BE VALID JSON ONLY. "
                    "DO NOT include any explanatory text, introductions, or descriptions before or after the JSON. "
                    "DO NOT use markdown code blocks or any other formatting. "
                    "JUST RETURN RAW JSON DATA OR THE STRING 'None'. "
                    "The key must be 'questions' not 'quiz', and each question must have 'content', 'options', 'answer', and 'explanation'. "
                    "The 'options' must be an object with keys A, B, C, D, not an array. "
                    'EXAMPLE OF CORRECT OUTPUT FORMAT: {"questions":[{"content":"Question text","options":{"A":"Option A","B":"Option B","C":"Option C","D":"Option D"},"answer":"A","explanation":"Explanation text"}]} '
                    "NEVER OUTPUT TEXT LIKE 'Here are the questions' OR 'The quiz is as follows'. "
                    "ONLY OUTPUT JSON OR 'None'."
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
    ) -> Quiz | None:
        """LangGraphを用いてクイズを生成する"""
        try:
            result = self.graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Generate {question_count} quiz questions of difficulty '{difficulty}'.",
                        }
                    ]
                }
            )

            for item in result["messages"]:
                print(f"Name: {item.name}")
                print(item.content)
                print("================")

            # デバッグ用にメッセージ構造をログ出力
            logger.debug("LangGraph messages structure:")
            for item in result["messages"]:
                if hasattr(item, "name"):
                    logger.debug(f"Message from {item.name}")

            # supervisorからの最終出力を処理
            for message in reversed(result["messages"]):
                if hasattr(message, "name") and message.name == "supervisor":
                    content = message.content
                    if (
                        content
                        and isinstance(content, str)
                        and content.strip() not in ["None", ""]
                    ):
                        try:
                            # JSONデータとして解析
                            data = json.loads(content)
                            if "questions" in data and isinstance(
                                data["questions"], list
                            ):
                                # 有効なクイズデータが見つかった
                                logger.info("Valid quiz data found from supervisor")
                                return Quiz(questions=data["questions"])
                        except json.JSONDecodeError:
                            logger.warning(
                                f"Failed to parse supervisor content as JSON: {content[:100]}..."
                            )

            # rag_quiz_agentの出力をチェック
            for message in result["messages"]:
                if hasattr(message, "name") and message.name == "rag_quiz_agent":
                    content = message.content
                    if (
                        content
                        and isinstance(content, str)
                        and content.strip() not in ["None", ""]
                    ):
                        try:
                            # JSONデータとして解析
                            if content.strip().startswith("{"):
                                data = json.loads(content)
                                if "questions" in data and isinstance(
                                    data["questions"], list
                                ):
                                    # RAGエージェントから有効なクイズデータが見つかった
                                    logger.info(
                                        "Valid quiz data found from rag_quiz_agent"
                                    )
                                    return Quiz(questions=data["questions"])
                        except json.JSONDecodeError:
                            logger.warning(
                                f"Failed to parse RAG agent content as JSON: {content[:100]}..."
                            )

            # 有効なクイズデータが見つからなかった場合
            logger.warning("No valid quiz data found from any source")
            return None

        except ValueError as e:
            error_msg = f"Failed to parse LLM response: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise LLMResponseParsingError(error_msg)

        except Exception as e:
            error_msg = f"Error while running LangGraph: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RAGChainExecutionError(error_msg)
