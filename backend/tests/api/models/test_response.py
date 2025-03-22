import pytest
from pydantic import ValidationError

from src.api.models.quiz import Quiz
from src.domain.entities.question import QuizOption


def valid_quiz_data() -> dict:
    """
    有効な Quiz のデータを返すヘルパー関数。
    """
    return {
        "content": "クイズの内容",
        "options": {"A": "選択肢 A", "B": "選択肢 B", "C": "選択肢 C", "D": "選択肢 D"},
        "answer": "A",
        "explanation": "解説",
    }


def test_valid_quiz_option():
    """QuizOption の有効なデータが正しく変換されることを確認"""
    data = {"A": "選択肢 A", "B": "選択肢 B", "C": "選択肢 C", "D": "選択肢 D"}
    option = QuizOption(**data)
    assert option.A == "選択肢 A"
    assert option.B == "選択肢 B"
    assert option.C == "選択肢 C"
    assert option.D == "選択肢 D"


def test_quiz_option_missing_field():
    """QuizOption の必須フィールドのうち、1つが欠如している場合に ValidationError が発生することを確認"""
    data = {
        "A": "選択肢 A",
        "B": "選択肢 B",
        # "C" フィールドが欠如
        "D": "選択肢 D",
    }
    with pytest.raises(ValidationError):
        QuizOption(**data)


def test_valid_quiz():
    """Quiz の有効なデータが正しく変換されることを確認"""
    quiz_data = valid_quiz_data()
    quiz = Quiz(**quiz_data)
    assert quiz.content == "クイズの内容"
    assert quiz.options.A == "選択肢 A"
    assert quiz.answer == "A"
    assert quiz.explanation == "解説"


def test_quiz_missing_fields():
    """Quiz の必須フィールドのうち、answer が欠如している場合に ValidationError が発生することを確認"""
    quiz_data = valid_quiz_data()
    del quiz_data["answer"]
    with pytest.raises(ValidationError):
        Quiz(**quiz_data)
