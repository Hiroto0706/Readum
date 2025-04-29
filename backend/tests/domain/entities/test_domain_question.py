import pytest
from pydantic import ValidationError

from src.domain.entities.question import QuizType, QuizOption, Question


class TestQuizType:
    def test_quiz_type_values(self):
        """QuizTypeの列挙値が正しいことを確認"""
        assert QuizType.TEXT.value == "text"
        assert QuizType.URL.value == "url"

    def test_quiz_type_from_string(self):
        """文字列からQuizTypeに変換できることを確認"""
        assert QuizType("text") == QuizType.TEXT
        assert QuizType("url") == QuizType.URL

    def test_invalid_quiz_type(self):
        """無効な値でQuizTypeを作成するとエラーになることを確認"""
        with pytest.raises(ValueError):
            QuizType("invalid_type")


class TestQuizOption:
    def test_valid_quiz_option(self):
        """有効なQuizOptionを作成できることを確認"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")

        assert options.A == "Option A"
        assert options.B == "Option B"
        assert options.C == "Option C"
        assert options.D == "Option D"

    def test_missing_options(self):
        """選択肢が不足している場合、ValidationErrorが発生することを確認"""
        with pytest.raises(ValidationError):
            QuizOption(A="Option A", B="Option B", C="Option C")

        with pytest.raises(ValidationError):
            QuizOption(A="Option A", B="Option B")

    def test_immutability(self):
        """QuizOptionがイミュータブル（変更不可）であることを確認"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")

        with pytest.raises(Exception):
            options.A = "Changed Option A"

    def test_extra_fields_ignored(self):
        """余分なフィールドが無視されることを確認"""
        options = QuizOption(
            A="Option A",
            B="Option B",
            C="Option C",
            D="Option D",
            E="Extra option",  # 余分なフィールド
        )

        assert not hasattr(options, "E")


class TestQuestion:
    def test_valid_question(self):
        """有効なQuestionを作成できることを確認"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")
        question = Question(
            question="What is the question?",
            options=options,
            answer="A",
            explanation="This is the explanation",
        )

        assert question.question == "What is the question?"
        assert question.options == options
        assert question.answer == "A"
        assert question.explanation == "This is the explanation"

    def test_missing_fields(self):
        """必須フィールドが欠けている場合、ValidationErrorが発生することを確認"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")

        # contentが欠けている
        with pytest.raises(ValidationError):
            Question(options=options, answer="A", explanation="This is the explanation")

        # optionsが欠けている
        with pytest.raises(ValidationError):
            Question(
                question="What is the question?",
                answer="A",
                explanation="This is the explanation",
            )

    def test_immutability(self):
        """Questionがイミュータブル（変更不可）であることを確認"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")
        question = Question(
            question="What is the question?",
            options=options,
            answer="A",
            explanation="This is the explanation",
        )

        with pytest.raises(Exception):
            question.question = "Changed question"

    def test_with_long_content(self):
        """長い質問内容でも正常に作成できることを確認"""
        options = QuizOption(A="Option A", B="Option B", C="Option C", D="Option D")
        long_content = "A" * 1000  # 1000文字の質問

        question = Question(
            question=long_content,
            options=options,
            answer="A",
            explanation="This is the explanation",
        )

        assert question.question == long_content

    def test_direct_dict_options(self):
        """辞書からオプションを作成できることを確認"""
        question = Question(
            question="What is the question?",
            options={
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D",
            },
            answer="A",
            explanation="This is the explanation",
        )

        assert question.options.A == "Option A"
        assert question.options.B == "Option B"
        assert question.options.C == "Option C"
        assert question.options.D == "Option D"
