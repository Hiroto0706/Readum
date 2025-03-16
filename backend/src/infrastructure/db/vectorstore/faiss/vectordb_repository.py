from typing import Any, List

from backend.src.domain.repositories.vectordb_interface import VectorStoreHandler


class VectorStoreHandlerImpl(VectorStoreHandler):
    """
    FAISSインデックスを操作するために必要なメソッドの実態をここで定義する
    """

    def embed_texts(self, texts: List[str]) -> Any:
        """
        テキストのリストを受け取り、ベクトル表現に変換します。
        """
        pass

    def save(self, directory: str) -> None:
        """
        ベクトルストアのデータを指定されたディレクトリに保存します。
        """
        pass

    def load(self, directory: str) -> "VectorStoreHandlerImpl":
        """
        指定されたディレクトリからベクトルストアのデータを読み込みます。
        """
        pass

    def as_retriever(self, search_kwargs: dict) -> Any:
        """
        ベクトルストアからリトリーバー（検索機能）を返します。
        """
        pass

    def _create_temp_directory(self) -> str:
        """
        一時ディレクトリを作成し、そのパスを返します。
        """
        pass

    def _delete_directory(self, directory: str) -> None:
        """
        指定されたディレクトリを削除します。
        """
        pass
