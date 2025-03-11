import pytest
from pydantic import ValidationError

from src.api.models.response import QuizOption, Quiz, QuizPreview, QuizResponse


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


def test_quiz_preview_valid_item_count():
    """
    QuizPreview が questions リストの要素数3件および20件の場合に正しく生成されることを確認。
    """
    # 最小件数（3件）のテスト
    quiz_list_min = [valid_quiz_data() for _ in range(3)]
    preview_min = QuizPreview(questions=quiz_list_min)
    assert len(preview_min.questions) == 3

    # 最大件数（20件）のテスト
    quiz_list_max = [valid_quiz_data() for _ in range(20)]
    preview_max = QuizPreview(questions=quiz_list_max)
    assert len(preview_max.questions) == 20


def test_quiz_preview_invalid_item_count_low():
    """QuizPreview の questions リストの要素数が3件未満の場合に ValidationError が発生することを確認"""
    quiz_list = [valid_quiz_data() for _ in range(2)]
    with pytest.raises(ValidationError):
        QuizPreview(questions=quiz_list)


def test_quiz_preview_invalid_item_count_high():
    """QuizPreview の questions リストの要素数が20件を超える場合に ValidationError が発生することを確認"""
    quiz_list = [valid_quiz_data() for _ in range(21)]
    with pytest.raises(ValidationError):
        QuizPreview(questions=quiz_list)


def test_valid_quiz_response():
    """QuizResponse が有効な QuizPreview をラップしていることを確認"""
    quiz_list = [valid_quiz_data() for _ in range(5)]
    preview_data = {"questions": quiz_list}
    response_data = {"preview": preview_data}
    response = QuizResponse(**response_data)
    assert isinstance(response.preview, QuizPreview)
    assert len(response.preview.questions) == 5


def test_quiz_response_missing_preview():
    """QuizResponse の preview フィールドが欠如している場合に ValidationError が発生することを確認"""
    response_data = {}
    with pytest.raises(ValidationError):
        QuizResponse(**response_data)
