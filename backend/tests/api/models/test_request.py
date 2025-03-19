import pytest
from pydantic import ValidationError
from src.api.models.request import QuizType, Difficulty, QuizRequest


def test_quiz_request_valid_text():
    """エイリアスキー 'questionCount' を使用した、有効なテキストクイズデータのテスト"""
    data = {
        "type": "text",
        "content": "これはサンプルのテキストクイズの内容です。",
        "difficulty": "beginner",
        "questionCount": 5,
    }
    quiz_request = QuizRequest(**data)
    assert quiz_request.type == QuizType.TEXT
    assert quiz_request.content == "これはサンプルのテキストクイズの内容です。"
    assert quiz_request.difficulty == Difficulty.BEGINNER
    assert quiz_request.question_count == 5


def test_quiz_request_valid_url():
    """有効なURLが設定された場合のテスト（URLタイプ）"""
    data = {
        "type": "url",
        "content": "https://example.com",
        "difficulty": "advanced",
        "questionCount": 10,
    }
    quiz_request = QuizRequest(**data)
    assert quiz_request.type == QuizType.URL
    assert quiz_request.content == "https://example.com"
    assert quiz_request.difficulty == Difficulty.ADVANCED
    assert quiz_request.question_count == 10


def test_quiz_request_using_field_name():
    """populate_by_name=True により、エイリアスではなくフィールド名を使用した場合のテスト"""
    data = {
        "type": "url",
        "content": "https://another-example.com",
        "difficulty": "intermediate",
        "question_count": 7,  # フィールド名で値を渡す
    }
    quiz_request = QuizRequest(**data)
    assert quiz_request.question_count == 7


def test_quiz_request_invalid_question_count_low():
    """質問数が最小値の3より小さい場合、ValidationError が発生するテスト"""
    data = {
        "type": "text",
        "content": "質問数が低すぎるテストのための内容。",
        "difficulty": "beginner",
        "questionCount": 2,  # 3未満 → エラーとなる
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)


def test_quiz_request_invalid_question_count_high():
    """質問数が最大値の20より大きい場合、ValidationError が発生するテスト"""
    data = {
        "type": "text",
        "content": "質問数が高すぎるテストのための内容。",
        "difficulty": "intermediate",
        "questionCount": 25,  # 20を超える → エラーとなる
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)


def test_quiz_request_invalid_difficulty():
    """許可されていない難易度が指定された場合、ValidationError が発生するテスト"""
    data = {
        "type": "text",
        "content": "無効な難易度のテスト。",
        "difficulty": "expert",  # 許可されていない値
        "questionCount": 5,
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)


def test_quiz_request_missing_field():
    """必須フィールド（difficulty）が欠如している場合、ValidationError が発生するテスト"""
    data = {
        "type": "url",
        "content": "https://incomplete-example.com",
        # "difficulty" フィールドが欠如
        "questionCount": 5,
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)


def test_quiz_request_invalid_url_format():
    """URLタイプの場合に、無効なURL形式が指定された場合、ValidationError が発生するテスト"""
    data = {
        "type": "url",
        "content": "invalid_url",  # httpやhttps以外のスキームもしくは不正なURL
        "difficulty": "advanced",
        "questionCount": 5,
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)


def test_quiz_request_using_enum_fields():
    """Enum型のインスタンスを直接渡した場合のテスト：QuizType と Difficulty"""
    data = {
        "type": QuizType.TEXT,  # Enumインスタンスを使用
        "content": "Enumインスタンスを直接渡すテスト",
        "difficulty": Difficulty.BEGINNER,  # Enumインスタンスを使用
        "questionCount": 7,
    }
    quiz_request = QuizRequest(**data)
    assert quiz_request.type == QuizType.TEXT
    assert quiz_request.difficulty == Difficulty.BEGINNER


def test_quiz_request_invalid_type_value():
    """無効なQuizTypeの値を指定した場合にValidationErrorとなるテスト"""
    data = {
        "type": "not_a_valid_type",  # 不正な値
        "content": "不正なタイプ値のテスト",
        "difficulty": "advanced",
        "questionCount": 5,
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)


def test_quiz_request_invalid_url_scheme_ftp():
    """URLタイプの場合に、許可されていないスキーム（ftp）の場合、ValidationError が発生するテスト"""
    data = {
        "type": "url",
        "content": "ftp://example.com",  # ftpスキームは許可されていない
        "difficulty": "advanced",
        "questionCount": 5,
    }
    with pytest.raises(ValidationError):
        QuizRequest(**data)
