import pytest
from pydantic import ValidationError
from src.domain.value_objects.quiz_content import (
    QuizContent,
    QuizType,
    QuizTypeEnum,
    QuizDifficulty,
    QuizDifficultyEnum,
    QuestionCount,
)


def test_quiz_content_valid():
    """
    先後の空白が除去され、かつ空にならない有効な文字列の場合、正常に生成されることを確認。
    """
    input_str = "  This is a valid quiz content.  "
    qc = QuizContent(value=input_str)
    # 空白が除去されるので期待値は前後の空白なしの文字列
    assert qc.value == "This is a valid quiz content."


def test_quiz_content_invalid_empty():
    """
    空文字あるいは空白のみでは、最小長の検証により ValidationError となることを確認。
    """
    with pytest.raises(ValidationError):
        QuizContent(value="     ")


def test_quiz_type_valid_string():
    """
    'text' あるいは 'url' といった有効な文字列を渡すと、Enum に変換されることを確認。
    """
    qt = QuizType(value="text")
    assert qt.value == QuizTypeEnum.TEXT


def test_quiz_type_valid_enum():
    """
    Enumのインスタンスそのものを渡した場合も、正しく生成されることを確認。
    """
    qt = QuizType(value=QuizTypeEnum.URL)
    assert qt.value == QuizTypeEnum.URL


def test_quiz_type_invalid():
    """
    無効な文字列を与えた場合、ValidationError となることを確認。
    """
    with pytest.raises(ValidationError):
        QuizType(value="invalid_type")


def test_quiz_difficulty_valid_string():
    """
    有効な難易度（文字列の場合）を渡すと、Enum に変換されることを確認。
    """
    qd = QuizDifficulty(value="intermediate")
    assert qd.value == QuizDifficultyEnum.INTERMEDIATE


def test_quiz_difficulty_valid_enum():
    """
    Enum のインスタンスそのものを渡した場合も、正しく生成されることを確認。
    """
    qd = QuizDifficulty(value=QuizDifficultyEnum.BEGINNER)
    assert qd.value == QuizDifficultyEnum.BEGINNER


def test_quiz_difficulty_invalid():
    """
    許可されていない難易度を渡した場合、ValidationError となることを確認。
    """
    with pytest.raises(ValidationError):
        QuizDifficulty(value="expert")


def test_question_count_valid_boundaries():
    """
    質問数の下限（3）および上限（20）の境界値が有効であることを確認。
    """
    qc_low = QuestionCount(value=3)
    qc_high = QuestionCount(value=20)
    assert qc_low.value == 3
    assert qc_high.value == 20


def test_question_count_too_low():
    """
    質問数が下限より小さい場合、ValidationError となることを確認。
    """
    with pytest.raises(ValidationError):
        QuestionCount(value=2)


def test_question_count_too_high():
    """
    質問数が上限より大きい場合、ValidationError となることを確認。
    """
    with pytest.raises(ValidationError):
        QuestionCount(value=21)
