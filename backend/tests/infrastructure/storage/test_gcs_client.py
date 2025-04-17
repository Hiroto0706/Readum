import json
import pytest

from google.cloud import storage

from src.infrastructure.storage.gcs_client import GCSClient
from config.settings import settings


class TestGCSClient:
    @pytest.fixture
    def mock_storage_client(self, mocker):
        """Google Cloud Storage クライアントのモックを作成するフィクスチャ"""
        # スペック準拠モデルの作成
        # スペック準拠モデルは元クラスに存在しないメソッドを呼び出そうとするとエラーを返す
        mock_client = mocker.MagicMock(spec=storage.Client)
        # パッチ適用
        # 指定したパスを一時的にモックに置き換える
        # コード内で指定したパスが呼ばれるとreturn_valueを返す
        mocker.patch("google.cloud.storage.Client", return_value=mock_client)
        return mock_client

    @pytest.fixture
    def mock_bucket(self, mocker):
        """GCS バケットのモックを作成するフィクスチャ"""
        mock_bucket = mocker.MagicMock(spec=storage.Bucket)
        return mock_bucket

    @pytest.fixture
    def mock_blob(self, mocker):
        """GCS ブロブのモックを作成するフィクスチャ"""
        mock_blob = mocker.MagicMock(spec=storage.Blob)
        return mock_blob

    @pytest.fixture
    def sample_user_answer(self):
        """テスト用のUserAnswerデータを作成するフィクスチャ"""
        return {
            "id": "test-quiz-id",
            "preview": {
                "questions": [
                    {
                        "content": "テスト質問1",
                        "options": {
                            "A": "選択肢A",
                            "B": "選択肢B",
                            "C": "選択肢C",
                            "D": "選択肢D",
                        },
                        "answer": "A",
                        "explanation": "テスト解説1",
                    }
                ]
            },
            "selectedOptions": ["A"],
            "difficultyValue": "intermediate",
        }

    # fixtureで定義したモックを受け取ることができる
    def test_init_existing_bucket(self, mock_storage_client, mock_bucket):
        """既存のバケットでGCSClientを初期化できることをテスト"""
        # get_bucketが呼ばれた時、mock_bucketを返すように設定する
        mock_storage_client.get_bucket.return_value = mock_bucket

        gcs_client = GCSClient()

        # get_bucket メソッドが、設定ファイルに定義されたバケット名で正確に1回だけ呼ばれたことをアサートする
        mock_storage_client.get_bucket.assert_called_once_with(
            settings.third_party.BUCKET_NAME
        )
        # 逆にこれは一度も呼ばれていないことをアサートする
        mock_storage_client.create_bucket.assert_not_called()
        assert gcs_client.bucket == mock_bucket
        assert gcs_client.bucket_name == settings.third_party.BUCKET_NAME
        assert gcs_client.prefix == f"{settings.app.ENV}/results/"

    def test_init_create_bucket(self, mock_storage_client, mock_bucket):
        """バケットが存在しない場合、新しいバケットを作成することをテスト"""
        # モックメソッドが呼ばれた時の副作用を設定する。これは実際のクラスと同じ挙動を再現するための設定
        mock_storage_client.get_bucket.side_effect = Exception("Bucket not found")
        # create_bucketが呼ばれた時、mock_bucketを返すように設定
        mock_storage_client.create_bucket.return_value = mock_bucket

        gcs_client = GCSClient()

        # Assert
        mock_storage_client.get_bucket.assert_called_once_with(
            settings.third_party.BUCKET_NAME
        )
        mock_storage_client.create_bucket.assert_called_once_with(
            settings.third_party.BUCKET_NAME
        )
        assert gcs_client.bucket == mock_bucket

    def test_save_quiz_success(
        self, mock_storage_client, mock_bucket, mock_blob, sample_user_answer
    ):
        """クイズデータを正常に保存できることをテスト"""
        # Arrange
        mock_storage_client.get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob

        gcs_client = GCSClient()
        quiz_id = "test-quiz-id"

        # ここでsave_quiz()を実行しているが、内部ではモックが実行されるだけ
        # レスポンスは実際のコードのものが返ってくる
        # 実際のコードではblob_nameを返しているのでresultはblob_nameとなるのだ
        result = gcs_client.save_quiz(quiz_id, sample_user_answer)

        expected_blob_name = f"{gcs_client.prefix}{quiz_id}.json"
        # 以下のアサートではpatchを用いて振る舞いをコピーしているので、呼ばれた回数がわかる
        mock_bucket.blob.assert_called_once_with(expected_blob_name)
        mock_blob.upload_from_string.assert_called_once()
        # call_args[0][0]で実コードのblob.upload_from_string()の第１引数を参照している
        # ちなみに第２引数を参照したい場合はcall_string[0][1]とすればよい
        upload_data = mock_blob.upload_from_string.call_args[0][0]
        assert json.loads(upload_data) == sample_user_answer
        assert result == expected_blob_name

    def test_save_quiz_failure(self, mock_storage_client, mock_bucket, mock_blob):
        """保存時にエラーが発生した場合の挙動をテスト"""
        # Arrange
        mock_storage_client.get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.upload_from_string.side_effect = Exception("Upload failed")

        gcs_client = GCSClient()
        quiz_id = "test-quiz-id"
        data = {"test": "data"}

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            gcs_client.save_quiz(quiz_id, data)

        assert "Upload failed" in str(exc_info.value)

    def test_get_result_success(
        self, mock_storage_client, mock_bucket, mock_blob, sample_user_answer
    ):
        """クイズ結果を正常に取得できることをテスト"""
        # Arrange
        mock_storage_client.get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.exists.return_value = True

        # JSONデータをモック
        mock_blob.download_as_text.return_value = json.dumps(sample_user_answer)

        gcs_client = GCSClient()
        quiz_id = "test-quiz-id"

        # Act
        result = gcs_client.get_result(quiz_id)

        # Assert
        expected_blob_name = f"{gcs_client.prefix}{quiz_id}.json"
        mock_bucket.blob.assert_called_once_with(expected_blob_name)
        mock_blob.exists.assert_called_once()
        mock_blob.download_as_text.assert_called_once()
        assert result == sample_user_answer

    def test_get_result_not_found(self, mock_storage_client, mock_bucket, mock_blob):
        """存在しないクイズIDに対してNoneを返すことをテスト"""
        # Arrange
        mock_storage_client.get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.exists.return_value = False

        gcs_client = GCSClient()
        quiz_id = "nonexistent-quiz-id"

        # Act
        result = gcs_client.get_result(quiz_id)

        # Assert
        mock_blob.download_as_text.assert_not_called()
        assert result is None

    def test_get_result_failure(self, mock_storage_client, mock_bucket, mock_blob):
        """取得時にエラーが発生した場合の挙動をテスト"""
        # Arrange
        mock_storage_client.get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.exists.return_value = True
        mock_blob.download_as_text.side_effect = Exception("Download failed")

        gcs_client = GCSClient()
        quiz_id = "test-quiz-id"

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            gcs_client.get_result(quiz_id)

        assert "Download failed" in str(exc_info.value)
