import pytest

from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.domain.entities.quiz import Quiz
from src.domain.entities.question import Question, QuizOption
from src.infrastructure.llm.rag_agent import RAGAgentModelImpl
from src.infrastructure.exceptions.llm_exceptions import (
    LLMResponseParsingError,
    RAGChainExecutionError,
    RAGChainSetupError,
)


class TestRAGAgentModelImpl:
    @pytest.fixture
    def mock_llm(self, mocker):
        """LLMモデルのモックを作成するフィクスチャ"""
        mock_llm = mocker.MagicMock(spec=ChatOpenAI)
        # with_structured_outputメソッドが新しいモックを返すように設定
        mock_structured_output = mocker.MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured_output
        return mock_llm

    @pytest.fixture
    def mock_prompt(self, mocker):
        """プロンプトテンプレートのモックを作成するフィクスチャ"""
        return mocker.MagicMock(spec=PromptTemplate)

    @pytest.fixture
    def mock_retriever(self, mocker):
        """VectorStoreRetrieverのモックを作成するフィクスチャ"""
        return mocker.MagicMock(spec=VectorStoreRetriever)

    @pytest.fixture
    def sample_quiz(self):
        """テスト用のQuizオブジェクトを作成するフィクスチャ"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")
        questions = [
            Question(
                content=f"Test question {i}",
                options=options,
                answer="A",
                explanation=f"Test explanation {i}",
            )
            for i in range(1, 4)  # 3問作成
        ]
        return Quiz(questions=questions)

    @pytest.fixture
    def rag_agent(self, mock_llm, mock_prompt, mock_retriever):
        """RAGAgentModelImplのインスタンスを作成するフィクスチャ"""
        return RAGAgentModelImpl(
            llm=mock_llm, prompt=mock_prompt, retriever=mock_retriever
        )

    # def test_set_rag_chain_success(self, rag_agent, mock_retriever, mocker):
    #     """RAG Chainの設定が成功するケースをテスト"""
    #     # itemgetterは実コード内で定義されており、テストコードからはアクセスできないためmock.patch()を使っている
    #     mocker.patch(
    #         "src.infrastructure.llm.rag_agent.itemgetter",
    #         return_value=mocker.MagicMock(),
    #     )

    #     # Act
    #     result = rag_agent.set_rag_chain(mock_retriever)

    #     # Assert
    #     assert result is not None
    #     assert isinstance(result, RAGAgentModelImpl)
    #     assert result.rag_chain is not None
    #     # LLMのwith_structured_outputが呼ばれたことを確認
    #     rag_agent.llm.with_structured_output.assert_called_once_with(Quiz)

    # def test_set_rag_chain_failure(self, rag_agent, mock_retriever, mocker):
    #     """RAG Chainの設定が失敗するケースをテスト"""
    #     # Arrange
    #     mocker.patch(
    #         "src.infrastructure.llm.rag_agent.itemgetter",
    #         side_effect=Exception("Mock itemgetter error"),
    #     )

    #     # Act & Assert
    #     with pytest.raises(RAGChainSetupError) as exc_info:
    #         rag_agent.set_rag_chain(mock_retriever)

    #     assert "Failed to set up RAG chain" in str(exc_info.value)
    #     assert "Mock itemgetter error" in str(exc_info.value)

    def test_invoke_chain_success(self, rag_agent, sample_quiz, mocker):
        """RAG Chainの実行が成功するケースをテスト"""
        # Arrange
        mock_chain = mocker.MagicMock()
        mock_chain.invoke.return_value = sample_quiz
        rag_agent.rag_chain = mock_chain

        # Act
        result = rag_agent.invoke_chain(question_count=3, difficulty="intermediate")

        # Assert
        assert result == sample_quiz
        mock_chain.invoke.assert_called_once()
        # invoke呼び出しの引数を検証
        call_args = mock_chain.invoke.call_args[0][0]
        assert call_args["question_count"] == 3
        assert call_args["difficulty"] == "intermediate"
        assert "input" in call_args

    def test_invoke_chain_without_initialization(self, rag_agent):
        """初期化されていないRAG Chainを実行しようとするケースをテスト"""
        # Arrange
        rag_agent.rag_chain = None

        # Act & Assert
        with pytest.raises(RAGChainExecutionError) as exc_info:
            rag_agent.invoke_chain(question_count=3, difficulty="intermediate")

        assert "RAG chain is not initialized" in str(exc_info.value)

    def test_invoke_chain_parsing_error(self, rag_agent, mocker):
        """LLMレスポンスのパース中にエラーが発生するケースをテスト"""
        # Arrange
        mock_chain = mocker.MagicMock()
        mock_chain.invoke.side_effect = ValueError("Invalid response format")
        rag_agent.rag_chain = mock_chain

        # Act & Assert
        with pytest.raises(LLMResponseParsingError) as exc_info:
            rag_agent.invoke_chain(question_count=3, difficulty="intermediate")

        assert "Failed to parse LLM response" in str(exc_info.value)

    def test_invoke_chain_execution_error(self, rag_agent, mocker):
        """RAG Chain実行中に一般的なエラーが発生するケースをテスト"""
        # Arrange
        mock_chain = mocker.MagicMock()
        mock_chain.invoke.side_effect = Exception("Chain execution failed")
        rag_agent.rag_chain = mock_chain

        # Act & Assert
        with pytest.raises(RAGChainExecutionError) as exc_info:
            rag_agent.invoke_chain(question_count=3, difficulty="intermediate")

        assert "Error while invoking RAG Chain" in str(exc_info.value)
        assert "Chain execution failed" in str(exc_info.value)
