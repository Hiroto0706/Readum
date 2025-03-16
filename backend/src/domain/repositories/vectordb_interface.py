from abc import ABC, abstractmethod
from typing import Any, List


class VectorStoreHandler(ABC):
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> Any:
        """
        テキストのリストを受け取り、ベクトル表現に変換します。
        """
        pass

    @abstractmethod
    def save(self, directory: str) -> None:
        """
        ベクトルストアのデータを指定されたディレクトリに保存します。
        """
        pass

    @abstractmethod
    def load(self, directory: str) -> "VectorStoreHandler":
        """
        指定されたディレクトリからベクトルストアのデータを読み込みます。
        """
        pass

    @abstractmethod
    def as_retriever(self, search_kwargs: dict) -> Any:
        """
        ベクトルストアからリトリーバー（検索機能）を返します。
        """
        pass

    @abstractmethod
    def _create_temp_directory(self) -> str:
        """
        一時ディレクトリを作成し、そのパスを返します。
        """
        pass

    @abstractmethod
    def _delete_directory(self, directory: str) -> None:
        """
        指定されたディレクトリを削除します。
        """
        pass
