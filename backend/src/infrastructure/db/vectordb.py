import logging
import os
from typing import List
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from src.infrastructure.exceptions.vectordb_exceptions import (
    InvalidDocumentError,
    VectorStoreCreationError,
    VectorStoreLoadError,
    VectorStoreNotInitializedError,
    VectorStoreSaveError,
)
from src.domain.repositories.vectordb_repository import VectorStoreHandler

from config.settings import Settings


logger = logging.getLogger(__name__)


@dataclass(frozen=True, config=ConfigDict(arbitrary_types_allowed=True))
class VectorStoreHandlerImpl(VectorStoreHandler):
    """
    FAISSインデックスを操作するために必要なメソッドの実態をここで定義する
    """

    embeddings_model: OpenAIEmbeddings
    vectorstore: None | FAISS

    def set_vectorstore(self, document: List[Document]) -> "VectorStoreHandlerImpl":
        if not document:
            error_msg = "Cannot create vectorstore from empty document list"
            logger.error(error_msg)
            raise InvalidDocumentError(error_msg)

        try:
            vectorstore = FAISS.from_documents(document, self.embeddings_model)

            return VectorStoreHandlerImpl(
                embeddings_model=self.embeddings_model,
                vectorstore=vectorstore,
            )

        except ValueError as e:
            error_msg = f"Invalid document format: {str(e)}"
            logger.error(error_msg)
            raise InvalidDocumentError(error_msg)

        except Exception as e:
            error_msg = f"Failed to create vectorstore: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise VectorStoreCreationError(error_msg)

    def save_local(self, dir_path: str) -> None:
        """
        ベクトルストアのデータを指定されたディレクトリに保存します。
        """
        if not self.vectorstore:
            error_msg = "Vectorstore instance is not initialized"
            logger.error(error_msg)
            raise VectorStoreNotInitializedError(error_msg)

        if not dir_path:
            error_msg = "Directory path cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            # ディレクトリが存在するか確認
            if not os.path.exists(dir_path):
                logger.info(f"Creating directory: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)

            self.vectorstore.save_local(dir_path)
            logger.info(f"Successfully saved vectorstore to {dir_path}")

        except Exception as e:
            error_msg = f"Failed to save vectorstore to {dir_path}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise VectorStoreSaveError(error_msg)

    def as_retriever(self, dir_path: str) -> VectorStoreRetriever:
        """
        ベクトルストアからリトリーバー（検索機能）を返します。
        """

        if not dir_path:
            error_msg = "Directory path cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not os.path.exists(dir_path):
            error_msg = f"Vectorstore directory does not exist: {dir_path}"
            logger.error(error_msg)
            raise VectorStoreLoadError(error_msg)

        try:
            vectorstore = FAISS.load_local(
                dir_path, self.embeddings_model, allow_dangerous_deserialization=True
            )
            retriever = vectorstore.as_retriever(
                search_kwargs={"k": Settings.embeddings.SEARCH_KWARGS}
            )
            logger.info(
                f"Successfully loaded vectorstore from {dir_path} and created retriever"
            )
            return retriever

        except FileNotFoundError as e:
            error_msg = f"Vectorstore files not found in {dir_path}: {str(e)}"
            logger.error(error_msg)
            raise VectorStoreLoadError(error_msg)

        except Exception as e:
            error_msg = f"Failed to load vectorstore from {dir_path}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise VectorStoreLoadError(error_msg)
