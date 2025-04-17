import pytest

from src.domain.entities.quiz import Quiz
from src.domain.entities.question import Question, QuizOption


# テスト用のQuestion作成ヘルパー関数
def create_test_question(content="Test Question", answer="A"):
    options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")
    return Question(
        content=content, options=options, answer=answer, explanation="Test explanation"
    )


class TestQuiz:
    def test_valid_quiz_creation(self):
        """有効なQuizオブジェクトを作成できることを確認"""
        # 5問のテスト質問を作成
        questions = [create_test_question(f"Question {i}", "A") for i in range(1, 6)]

        quiz = Quiz(questions=questions)

        assert len(quiz.questions) == 5
        assert quiz.questions[0].content == "Question 1"
        assert quiz.questions[4].content == "Question 5"

    def test_quiz_with_minimum_questions(self):
        """最小数（3問）の質問でQuizを作成できることを確認"""
        questions = [create_test_question(f"Question {i}", "A") for i in range(1, 4)]

        quiz = Quiz(questions=questions)

        assert len(quiz.questions) == 3

    def test_quiz_with_maximum_questions(self):
        """最大数（20問）の質問でQuizを作成できることを確認"""
        questions = [create_test_question(f"Question {i}", "A") for i in range(1, 21)]

        quiz = Quiz(questions=questions)

        assert len(quiz.questions) == 20

    def test_quiz_with_too_few_questions(self):
        """質問数が少なすぎる場合にエラーが発生することを確認"""
        # 2問しかない（3問未満）
        questions = [create_test_question(f"Question {i}", "A") for i in range(1, 3)]

        with pytest.raises(ValueError) as exc_info:
            Quiz(questions=questions)

        assert "質問は3問から20問の範囲である必要があります" in str(exc_info.value)

    def test_quiz_with_too_many_questions(self):
        """質問数が多すぎる場合にエラーが発生することを確認"""
        # 21問ある（20問超過）
        questions = [create_test_question(f"Question {i}", "A") for i in range(1, 22)]

        with pytest.raises(ValueError) as exc_info:
            Quiz(questions=questions)

        assert "質問は3問から20問の範囲である必要があります" in str(exc_info.value)

    def test_quiz_immutability(self):
        """Quizオブジェクトが不変であることを確認"""
        questions = [create_test_question(f"Question {i}", "A") for i in range(1, 6)]
        quiz = Quiz(questions=questions)

        with pytest.raises(Exception):
            quiz.questions = []  # 変更を試みる

    def test_quiz_with_varying_answer_options(self):
        """異なる回答を持つ質問でQuizを作成できることを確認"""
        q1 = create_test_question("Question 1", "A")
        q2 = create_test_question("Question 2", "B")
        q3 = create_test_question("Question 3", "C")
        q4 = create_test_question("Question 4", "D")

        quiz = Quiz(questions=[q1, q2, q3, q4])

        assert quiz.questions[0].answer == "A"
        assert quiz.questions[1].answer == "B"
        assert quiz.questions[2].answer == "C"
        assert quiz.questions[3].answer == "D"

    def test_empty_questions_list(self):
        """空の質問リストでエラーが発生することを確認"""
        with pytest.raises(ValueError):
            Quiz(questions=[])


# クイズに関する追加の検証テスト
def test_question_references():
    """Quizオブジェクト内のQuestion参照が保持されることを確認"""
    original_questions = [
        create_test_question(f"Question {i}", "A") for i in range(1, 4)
    ]
    quiz = Quiz(questions=original_questions)

    # 元の質問リストと、クイズ内の質問が同じオブジェクトを参照していることを確認
    for i, question in enumerate(original_questions):
        assert quiz.questions[i] is question
