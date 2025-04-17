import pytest
from pydantic import ValidationError

from src.domain.entities.results import UserAnswer
from src.domain.entities.quiz import Quiz
from src.domain.entities.question import Question, QuizOption


# テスト用のQuestion作成ヘルパー関数
def create_test_question(content="Test Question", answer="A"):
    options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")
    return Question(
        content=content, options=options, answer=answer, explanation="Test explanation"
    )


# テスト用のQuiz作成ヘルパー関数
def create_test_quiz(question_count=5):
    questions = [
        create_test_question(f"Question {i}", "A") for i in range(1, question_count + 1)
    ]
    return Quiz(questions=questions)


class TestUserAnswer:
    def test_valid_user_answer(self):
        """有効なUserAnswerオブジェクトを作成できることを確認"""
        quiz = create_test_quiz(5)
        user_answer = UserAnswer(
            id="test-id-123",
            preview=quiz,
            selected_options=["A", "B", "C", "D", "A"],
        )

        assert user_answer.id == "test-id-123"
        assert user_answer.preview == quiz
        assert user_answer.selected_options == ["A", "B", "C", "D", "A"]

    def test_mismatch_answer_count(self):
        """回答数と問題数が一致しない場合エラーになることを確認"""
        quiz = create_test_quiz(5)

        with pytest.raises(ValueError) as exc_info:
            UserAnswer(
                id="test-id-123",
                preview=quiz,
                selected_options=["A", "B", "C"],  # 5問に対して3回答
            )

        error_message = str(exc_info.value)
        assert "選択された回答の数" in error_message
        assert "一致しません" in error_message

    def test_invalid_option_values(self):
        """無効な回答オプションでエラーになることを確認"""
        quiz = create_test_quiz(3)

        with pytest.raises(ValueError) as exc_info:
            UserAnswer(
                id="test-id-123",
                preview=quiz,
                selected_options=["A", "X", "C"],  # Xは無効
            )

        error_message = str(exc_info.value)
        assert "無効な回答" in error_message or "有効な回答" in error_message

    def test_empty_id(self):
        """空のIDでエラーになることを確認"""
        quiz = create_test_quiz(3)

        with pytest.raises(ValueError):
            UserAnswer(id="", preview=quiz, selected_options=["A", "B", "C"])  # 空のID

    def test_immutability(self):
        """UserAnswerオブジェクトが不変であることを確認"""
        quiz = create_test_quiz(3)
        user_answer = UserAnswer(
            id="test-id-123", preview=quiz, selected_options=["A", "B", "C"]
        )

        with pytest.raises((TypeError, ValidationError)):
            user_answer.selected_options = ["D", "D", "D"]
