import os
import re
import uuid
import pytest

from src.application.usecase.quiz_creator import QuizCreator
from src.api.models.quiz import QuizType, Difficulty, QuizResponse
from src.domain.entities.quiz import Quiz
from src.application.exceptions.quiz_creation_exceptions import (
    RAGProcessingError,
)
from src.infrastructure.exceptions.llm_exceptions import (
    RAGChainSetupError,
    RAGChainExecutionError,
    LLMResponseParsingError,
)
from src.infrastructure.exceptions.vectordb_exceptions import (
    VectorStoreLoadError,
)

# テスト用の環境変数設定
os.environ["ENV"] = "test"
os.environ["LANGCHAIN_PROJECT"] = "readum-test"
os.environ["GPT_MODEL"] = "gpt-4.1-nano"


# テスト用のドキュメントパス
# プロジェクトルートからの絶対パス
DOCUMENT_PATH = os.path.abspath("assets/document.txt")


class TestQuizCreator:
    @pytest.fixture
    def quiz_creator(self):
        """QuizCreatorのインスタンスを作成するフィクスチャ"""
        return QuizCreator()

    def test_create_quiz_with_different_parameters(self, quiz_creator):
        """異なるパラメータでのクイズ作成をテスト"""
        # テスト用のドキュメントを読み込み
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # 様々なパラメータの組み合わせをテスト
        parameters = [
            (3, Difficulty.BEGINNER),
            (5, Difficulty.INTERMEDIATE),
            (7, Difficulty.ADVANCED),
        ]

        for question_count, difficulty in parameters:
            # クイズを生成
            response = quiz_creator.create_quiz(
                quiz_type=QuizType.TEXT,
                content=content,
                question_count=question_count,
                difficulty=difficulty,
            )

            # 返り値の検証
            self._validate_quiz_response(response, question_count, difficulty)

            # ベクトルストアディレクトリの削除を確認
            # 固有のIDを使ってディレクトリを検索する代わりに、一時ディレクトリが空かどうかチェック
            from config.settings import settings

            tmp_path = settings.embeddings.TMP_VECTORDB_PATH

            # IDごとのディレクトリが削除されているはずなので、
            # そのIDに対応するディレクトリは存在しないはず
            vector_dir = os.path.join(tmp_path, response.id)
            assert not os.path.exists(
                vector_dir
            ), f"ディレクトリが削除されていません: {vector_dir}"

    def test_process_rag_success(self, quiz_creator):
        """_process_ragメソッドの正常系テスト"""
        # テスト用のドキュメントを読み込み
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # ドキュメント処理とベクトルストア設定を実行
        from src.application.usecase.quiz_creator import DBFileHandlerImpl

        db_file_handler = DBFileHandlerImpl()

        temp_uuid = uuid.uuid4().hex

        # _process_documentの実行
        splitted_doc = quiz_creator._process_document(QuizType.TEXT, content)

        # _setup_vector_storeの実行
        vector_store_handler, directory_path = quiz_creator._setup_vector_store(
            splitted_doc, db_file_handler, temp_uuid
        )

        try:
            # _process_ragの実行
            question_count = 5
            difficulty = Difficulty.INTERMEDIATE
            response = quiz_creator._process_rag(
                vector_store_handler,
                directory_path,
                question_count,
                difficulty,
                temp_uuid,
            )

            # 返り値の検証
            self._validate_quiz_response(response, question_count, difficulty)

        finally:
            # リソースのクリーンアップ
            quiz_creator._cleanup_resources(directory_path, db_file_handler, temp_uuid)

    def test_rag_chain_setup_error(self, quiz_creator, mocker):
        """RAGChainSetupErrorのテスト"""
        # テスト用のドキュメントを読み込み
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # RAGAgentModelImpl.set_rag_chainをモックしてエラーを発生させる
        mocker.patch(
            "src.infrastructure.llm.rag_agent.RAGAgentModelImpl.set_rag_chain",
            side_effect=RAGChainSetupError("Test RAG chain setup error"),
        )

        # 例外が発生することを確認
        with pytest.raises(RAGProcessingError) as exc_info:
            quiz_creator.create_quiz(
                quiz_type=QuizType.TEXT,
                content=content,
                question_count=5,
                difficulty=Difficulty.INTERMEDIATE,
            )

        # エラーメッセージの検証
        error_msg = str(exc_info.value)
        assert "RAG processing failed" in error_msg
        assert "Test RAG chain setup error" in error_msg

    def test_rag_chain_execution_error(self, quiz_creator, mocker):
        """RAGChainExecutionErrorのテスト"""
        # テスト用のドキュメントを読み込み
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # RAGAgentModelImpl.invoke_chainをモックしてエラーを発生させる
        mocker.patch(
            "src.infrastructure.llm.rag_agent.RAGAgentModelImpl.invoke_chain",
            side_effect=RAGChainExecutionError("Test RAG chain execution error"),
        )

        # 例外が発生することを確認
        with pytest.raises(RAGProcessingError) as exc_info:
            quiz_creator.create_quiz(
                quiz_type=QuizType.TEXT,
                content=content,
                question_count=5,
                difficulty=Difficulty.INTERMEDIATE,
            )

        # エラーメッセージの検証
        error_msg = str(exc_info.value)
        assert "RAG processing failed" in error_msg
        assert "Test RAG chain execution error" in error_msg

    def test_llm_response_parsing_error(self, quiz_creator, mocker):
        """LLMResponseParsingErrorのテスト"""
        # テスト用のドキュメントを読み込み
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # RAGAgentModelImpl.invoke_chainをモックしてエラーを発生させる
        mocker.patch(
            "src.infrastructure.llm.rag_agent.RAGAgentModelImpl.invoke_chain",
            side_effect=LLMResponseParsingError("Test LLM response parsing error"),
        )

        # 例外が発生することを確認
        with pytest.raises(RAGProcessingError) as exc_info:
            quiz_creator.create_quiz(
                quiz_type=QuizType.TEXT,
                content=content,
                question_count=5,
                difficulty=Difficulty.INTERMEDIATE,
            )

        # エラーメッセージの検証
        error_msg = str(exc_info.value)
        assert "RAG processing failed" in error_msg
        assert "Test LLM response parsing error" in error_msg

    def test_vector_store_load_error(self, quiz_creator, mocker):
        """VectorStoreLoadErrorのテスト"""
        # テスト用のドキュメントを読み込み
        with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # VectorStoreHandlerImpl.as_retrieverをモックしてエラーを発生させる
        mocker.patch(
            "src.infrastructure.db.vectordb.VectorStoreHandlerImpl.as_retriever",
            side_effect=VectorStoreLoadError("Test vector store load error"),
        )

        # 例外が発生することを確認
        with pytest.raises(RAGProcessingError) as exc_info:
            quiz_creator.create_quiz(
                quiz_type=QuizType.TEXT,
                content=content,
                question_count=5,
                difficulty=Difficulty.INTERMEDIATE,
            )

        # エラーメッセージの検証
        error_msg = str(exc_info.value)
        assert "RAG processing failed" in error_msg
        assert "Test vector store load error" in error_msg

    def _validate_quiz_response(self, response, question_count, difficulty):
        """QuizResponseオブジェクトの検証を行うヘルパーメソッド"""
        # レスポンスの型を確認
        assert isinstance(response, QuizResponse)

        # IDがnullでないことだけ確認
        assert response.id, "Quiz IDがありません"

        # プレビューがQuizオブジェクトであることを確認
        assert isinstance(response.preview, Quiz)

        # 質問数が期待通りであることを確認
        assert len(response.preview.questions) == question_count

        # 難易度が期待通りであることを確認
        assert response.difficulty_value == difficulty.value

    def _is_valid_uuid(self, uuid_string):
        """文字列がUUIDフォーマットか検証するヘルパーメソッド"""
        uuid_pattern = re.compile(
            r"^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$",
            re.IGNORECASE,
        )
        return bool(uuid_pattern.match(uuid_string))
