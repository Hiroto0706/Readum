import pytest
from pydantic import ValidationError

from src.api.models.quiz import (
    QuizType,
    Difficulty,
    QuizRequest,
    Options,
    Question,
    Quiz,
    QuizResponse,
    UserAnswer,
)
from src.domain.entities.question import Question as DomainQuestion
from src.domain.entities.quiz import Quiz as DomainQuiz


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


class TestDifficulty:
    def test_difficulty_values(self):
        """Difficultyの列挙値が正しいことを確認"""
        assert Difficulty.BEGINNER.value == "beginner"
        assert Difficulty.INTERMEDIATE.value == "intermediate"
        assert Difficulty.ADVANCED.value == "advanced"

    def test_difficulty_from_string(self):
        """文字列からDifficultyに変換できることを確認"""
        assert Difficulty("beginner") == Difficulty.BEGINNER
        assert Difficulty("intermediate") == Difficulty.INTERMEDIATE
        assert Difficulty("advanced") == Difficulty.ADVANCED

    def test_invalid_difficulty(self):
        """無効な値でDifficultyを作成するとエラーになることを確認"""
        with pytest.raises(ValueError):
            Difficulty("invalid_difficulty")


class TestQuizRequest:
    def test_valid_text_request(self):
        """有効なテキストタイプのQuizRequestを作成できることを確認"""
        request = QuizRequest(
            type=QuizType.TEXT,
            content="テストコンテンツ",
            difficulty=Difficulty.INTERMEDIATE,
            questionCount=5,
        )

        assert request.type == QuizType.TEXT
        assert request.content == "テストコンテンツ"
        assert request.difficulty == Difficulty.INTERMEDIATE
        assert request.question_count == 5

    def test_valid_url_request(self):
        """有効なURLタイプのQuizRequestを作成できることを確認"""
        request = QuizRequest(
            type=QuizType.URL,
            content="https://example.com",
            difficulty=Difficulty.BEGINNER,
            questionCount=10,
        )

        assert request.type == QuizType.URL
        assert request.content == "https://example.com"
        assert request.difficulty == Difficulty.BEGINNER
        assert request.question_count == 10

    def test_empty_content(self):
        """空のコンテンツでエラーになることを確認"""
        with pytest.raises(ValueError) as exc_info:
            QuizRequest(
                type=QuizType.TEXT,
                content="",
                difficulty=Difficulty.INTERMEDIATE,
                questionCount=5,
            )

        assert "empty" in str(exc_info.value).lower()

    def test_whitespace_content(self):
        """空白のみのコンテンツでエラーになることを確認"""
        with pytest.raises(ValueError) as exc_info:
            QuizRequest(
                type=QuizType.TEXT,
                content="   ",
                difficulty=Difficulty.INTERMEDIATE,
                questionCount=5,
            )

        assert "empty" in str(exc_info.value).lower()

    def test_invalid_url_format(self):
        """URLタイプで無効なURL形式でエラーになることを確認"""
        with pytest.raises(ValueError) as exc_info:
            QuizRequest(
                type=QuizType.URL,
                content="invalid-url",
                difficulty=Difficulty.INTERMEDIATE,
                questionCount=5,
            )

        assert "valid url format" in str(exc_info.value).lower()

    def test_question_count_too_low(self):
        """問題数が少なすぎるとエラーになることを確認"""
        with pytest.raises(ValidationError) as exc_info:
            QuizRequest(
                type=QuizType.TEXT,
                content="テストコンテンツ",
                difficulty=Difficulty.INTERMEDIATE,
                questionCount=2,  # 最小値は3
            )

        assert "greater than or equal to 3" in str(
            exc_info.value
        ).lower() or "ge" in str(exc_info.value)

    def test_question_count_too_high(self):
        """問題数が多すぎるとエラーになることを確認"""
        with pytest.raises(ValidationError) as exc_info:
            QuizRequest(
                type=QuizType.TEXT,
                content="テストコンテンツ",
                difficulty=Difficulty.INTERMEDIATE,
                questionCount=21,  # 最大値は20
            )

        assert "less than or equal to 20" in str(exc_info.value).lower() or "le" in str(
            exc_info.value
        )

    def test_alias_question_count(self):
        """questionCountのエイリアスが機能することを確認"""
        request = QuizRequest(
            type=QuizType.TEXT,
            content="テストコンテンツ",
            difficulty=Difficulty.INTERMEDIATE,
            question_count=5,  # questionCountではなくquestion_countでも動作する
        )

        assert request.question_count == 5

    def test_immutability(self):
        """QuizRequestが不変であることを確認"""
        request = QuizRequest(
            type=QuizType.TEXT,
            content="テストコンテンツ",
            difficulty=Difficulty.INTERMEDIATE,
            questionCount=5,
        )

        with pytest.raises((ValidationError, TypeError)):
            request.content = "変更されたコンテンツ"


class TestOptions:
    def test_valid_options(self):
        """有効なOptionsを作成できることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        assert options.A == "選択肢A"
        assert options.B == "選択肢B"
        assert options.C == "選択肢C"
        assert options.D == "選択肢D"

    def test_missing_option(self):
        """選択肢が不足している場合にエラーになることを確認"""
        with pytest.raises(ValidationError):
            Options(
                A="選択肢A",
                B="選択肢B",
                C="選択肢C",
                # Dが欠けている
            )

    def test_immutability(self):
        """Optionsが不変であることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        with pytest.raises((ValidationError, TypeError)):
            options.A = "変更された選択肢A"

    def test_extra_fields_ignored(self):
        """余分なフィールドが無視されることを確認"""
        options = Options(
            A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D", E="無視される選択肢"
        )

        assert not hasattr(options, "E")


class TestQuestion:
    def test_valid_question(self):
        """有効なQuestionを作成できることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        question = Question(
            content="テスト質問", options=options, answer="A", explanation="テスト解説"
        )

        assert question.content == "テスト質問"
        assert question.options == options
        assert question.answer == "A"
        assert question.explanation == "テスト解説"

    def test_missing_fields(self):
        """必須フィールドが欠けている場合にエラーになることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        with pytest.raises(ValidationError):
            Question(
                # contentが欠けている
                options=options,
                answer="A",
                explanation="テスト解説",
            )

    def test_immutability(self):
        """Questionが不変であることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        question = Question(
            content="テスト質問", options=options, answer="A", explanation="テスト解説"
        )

        with pytest.raises((ValidationError, TypeError)):
            question.content = "変更された質問"

    def test_with_dictionary_options(self):
        """辞書形式のoptionsでも作成できることを確認"""
        question = Question(
            content="テスト質問",
            options={"A": "選択肢A", "B": "選択肢B", "C": "選択肢C", "D": "選択肢D"},
            answer="A",
            explanation="テスト解説",
        )

        assert isinstance(question.options, Options)
        assert question.options.A == "選択肢A"
        assert question.options.B == "選択肢B"


class TestQuiz:
    def test_valid_quiz(self):
        """有効なQuizを作成できることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 6)  # 5問
        ]

        quiz = Quiz(questions=questions)

        assert len(quiz.questions) == 5
        assert quiz.questions[0].content == "質問1"
        assert quiz.questions[4].content == "質問5"

    def test_minimum_questions(self):
        """最小問題数(3問)のQuizを作成できることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 4)  # 3問（最小値）
        ]

        quiz = Quiz(questions=questions)
        assert len(quiz.questions) == 3

    def test_maximum_questions(self):
        """最大問題数(20問)のQuizを作成できることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 21)  # 20問（最大値）
        ]

        quiz = Quiz(questions=questions)
        assert len(quiz.questions) == 20

    def test_too_few_questions(self):
        """問題数が少なすぎる場合にエラーになることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 3)  # 2問（最小は3問）
        ]

        with pytest.raises(ValidationError) as exc_info:
            Quiz(questions=questions)

        assert "min_length" in str(exc_info.value).lower() or "3" in str(exc_info.value)

    def test_too_many_questions(self):
        """問題数が多すぎる場合にエラーになることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 22)  # 21問（最大は20問）
        ]

        with pytest.raises(ValidationError) as exc_info:
            Quiz(questions=questions)

        assert "max_length" in str(exc_info.value).lower() or "20" in str(
            exc_info.value
        )

    def test_immutability(self):
        """Quizが不変であることを確認"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 6)
        ]

        quiz = Quiz(questions=questions)

        with pytest.raises((ValidationError, TypeError)):
            quiz.questions = []


class TestQuizResponse:
    @pytest.fixture
    def domain_quiz(self):
        """DomainQuizのテスト用フィクスチャ"""
        # DomainQuestionの作成
        domain_questions = [
            DomainQuestion(
                content=f"ドメイン質問{i}",
                options={"A": "選択A", "B": "選択B", "C": "選択C", "D": "選択D"},
                answer="A",
                explanation=f"ドメイン解説{i}",
            )
            for i in range(1, 6)
        ]

        # DomainQuizの作成
        return DomainQuiz(questions=domain_questions)

    def test_valid_quiz_response(self, domain_quiz):
        """有効なQuizResponseを作成できることを確認"""
        response = QuizResponse(
            id="test-id-123", preview=domain_quiz, difficultyValue="intermediate"
        )

        assert response.id == "test-id-123"
        assert response.preview == domain_quiz
        assert response.difficulty_value == "intermediate"

    def test_missing_fields(self, domain_quiz):
        """必須フィールドが欠けている場合にエラーになることを確認"""
        with pytest.raises(ValidationError):
            QuizResponse(
                # idが欠けている
                preview=domain_quiz,
                difficultyValue="intermediate",
            )

    def test_immutability(self, domain_quiz):
        """QuizResponseが不変であることを確認"""
        response = QuizResponse(
            id="test-id-123", preview=domain_quiz, difficultyValue="intermediate"
        )

        with pytest.raises((ValidationError, TypeError)):
            response.id = "new-id-456"


class TestUserAnswer:
    @pytest.fixture
    def test_quiz(self):
        """テスト用のQuizフィクスチャ"""
        options = Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D")

        questions = [
            Question(
                content=f"質問{i}", options=options, answer="A", explanation=f"解説{i}"
            )
            for i in range(1, 6)  # 5問
        ]

        return Quiz(questions=questions)

    def test_valid_user_answer(self, test_quiz):
        """有効なUserAnswerを作成できることを確認"""
        user_answer = UserAnswer(
            id="test-id-123",
            preview=test_quiz,
            selectedOptions=["A", "B", "C", "D", "A"],
            difficultyValue="intermediate",
        )

        assert user_answer.id == "test-id-123"
        assert user_answer.preview == test_quiz
        assert user_answer.selected_options == ["A", "B", "C", "D", "A"]
        assert user_answer.difficulty_value == "intermediate"

    def test_missing_fields(self, test_quiz):
        """必須フィールドが欠けている場合にエラーになることを確認"""
        with pytest.raises(ValidationError):
            UserAnswer(
                # idが欠けている
                preview=test_quiz,
                selectedOptions=["A", "B", "C", "D", "A"],
                difficultyValue="intermediate",
            )

    def test_invalid_option_length(self, test_quiz):
        """回答の数が問題と一致しない場合にエラーになることを確認"""
        with pytest.raises(ValueError) as exc_info:
            UserAnswer(
                id="test-id-123",
                preview=test_quiz,
                selectedOptions=["A", "B", "C"],  # 回答が3つしかない（問題は5つ）
                difficultyValue="intermediate",
            )

        assert "回答の数" in str(exc_info.value) or "一致しません" in str(
            exc_info.value
        )

    def test_invalid_option_values(self, test_quiz):
        """無効な選択肢がある場合にエラーになることを確認"""
        with pytest.raises(ValueError) as exc_info:
            UserAnswer(
                id="test-id-123",
                preview=test_quiz,
                selectedOptions=["A", "B", "C", "D", "E"],  # Eは無効
                difficultyValue="intermediate",
            )

        assert "無効な回答" in str(exc_info.value) or "E" in str(exc_info.value)

    def test_immutability(self, test_quiz):
        """UserAnswerが不変であることを確認"""
        user_answer = UserAnswer(
            id="test-id-123",
            preview=test_quiz,
            selectedOptions=["A", "B", "C", "D", "A"],
            difficultyValue="intermediate",
        )

        with pytest.raises((ValidationError, TypeError)):
            user_answer.selected_options = ["B", "B", "B", "B", "B"]
