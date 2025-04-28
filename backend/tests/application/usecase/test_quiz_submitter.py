import pytest

from src.application.usecase.quiz_submitter import QuizSubmitter
from src.application.exceptions.quiz_submit_exceptions import SaveObjectToStorageError
from src.infrastructure.storage.gcs_client import GCSClient
from src.api.models.quiz import UserAnswer, Quiz, Question, Options


class TestQuizSubmitter:
    @pytest.fixture
    def mock_gcs_client(self, mocker):
        """GCSClientのモックを作成するフィクスチャ"""
        mock_client = mocker.MagicMock(spec=GCSClient)
        # GCSClientのコンストラクタをモック化
        mocker.patch(
            "src.application.usecase.quiz_submitter.GCSClient", return_value=mock_client
        )
        return mock_client

    @pytest.fixture
    def sample_user_answer(self):
        """テスト用のUserAnswerオブジェクトを作成するフィクスチャ"""
        # Quizオブジェクトを作成
        quiz = Quiz(
            questions=[
                Question(
                    question=f"テスト質問{i}",
                    options=Options(A="選択肢A", B="選択肢B", C="選択肢C", D="選択肢D"),
                    answer="A",
                    explanation=f"テスト解説{i}",
                )
                for i in range(1, 4)
            ]
        )

        # UserAnswerオブジェクトを作成
        return UserAnswer(
            id="test-quiz-id",
            preview=quiz,
            selectedOptions=["A", "A", "A"],
            difficultyValue="intermediate",
        )

    def test_init_quiz_submitter(self, mock_gcs_client, sample_user_answer):
        """QuizSubmitterの初期化をテスト"""
        # QuizSubmitterをインスタンス化
        submitter = QuizSubmitter(user_answer=sample_user_answer)

        # 初期化を検証
        assert submitter.user_answer == sample_user_answer
        assert submitter.storage_client == mock_gcs_client

        # GCSClientのコンストラクタが呼ばれたことを確認
        from src.application.usecase.quiz_submitter import GCSClient

        GCSClient.assert_called_once()

    def test_save_object_to_storage_success(self, mock_gcs_client, sample_user_answer):
        """save_object_to_storageの正常系をテスト"""
        # GCSClientのsave_quizメソッドの戻り値を設定
        mock_gcs_client.save_quiz.return_value = "storage/path/test-quiz-id.json"

        # QuizSubmitterをインスタンス化
        submitter = QuizSubmitter(user_answer=sample_user_answer)

        # save_object_to_storageを実行
        result = submitter.save_object_to_storage()

        # 戻り値がNoneであることを確認
        assert result is None

        # save_quizが正しい引数で呼ばれたことを確認
        mock_gcs_client.save_quiz.assert_called_once_with(
            "test-quiz-id", sample_user_answer.model_dump()
        )

    def test_save_object_to_storage_failure(self, mock_gcs_client, sample_user_answer):
        """save_object_to_storageの異常系（例外発生）をテスト"""
        # GCSClientのsave_quizメソッドが例外を投げるように設定
        mock_gcs_client.save_quiz.side_effect = Exception("Storage error")

        # QuizSubmitterをインスタンス化
        submitter = QuizSubmitter(user_answer=sample_user_answer)

        # save_object_to_storageが例外を投げることを確認
        with pytest.raises(SaveObjectToStorageError) as exc_info:
            submitter.save_object_to_storage()

        # 例外メッセージを検証
        assert "Failed to save object to storage" in str(exc_info.value)
        assert "Storage error" in str(exc_info.value)

        # save_quizが呼ばれたことを確認
        mock_gcs_client.save_quiz.assert_called_once()

    def test_user_answer_model_dump_error(
        self, mock_gcs_client, sample_user_answer, mocker
    ):
        """UserAnswerのmodel_dumpでエラーが発生した場合のテスト"""
        # model_dumpメソッドがエラーを投げるようにモック
        mocker.patch(
            "src.api.models.quiz.UserAnswer.model_dump",
            side_effect=Exception("Serialization error"),
        )

        # QuizSubmitterをインスタンス化
        submitter = QuizSubmitter(user_answer=sample_user_answer)

        # save_object_to_storageが例外を投げることを確認
        with pytest.raises(SaveObjectToStorageError) as exc_info:
            submitter.save_object_to_storage()

        # 例外メッセージを検証
        assert "Failed to save object to storage" in str(exc_info.value)
        assert "Serialization error" in str(exc_info.value)

        # save_quizが呼ばれていないことを確認（model_dumpでエラーが起きるため）
        mock_gcs_client.save_quiz.assert_not_called()
