from fastapi import HTTPException, status


class BadRequestError(HTTPException):
    """リクエストが不正な場合のエラー"""

    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFoundError(HTTPException):
    """リソースが見つからない場合のエラー"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InternalServerError(HTTPException):
    """サーバー内部エラー"""

    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


# アプリケーション層の例外とHTTP例外のマッピング
def handle_application_exception(exception):
    """アプリケーション層の例外をHTTP例外に変換する"""
    from src.application.exceptions.quiz_creation_exceptions import (
        InvalidInputError,
        DocumentProcessingError,
        VectorStoreOperationError,
        RAGProcessingError,
    )
    from src.application.exceptions.quiz_submit_exceptions import (
        SaveObjectToStorageError,
    )
    from src.application.exceptions.get_result_exceptions import (
        ResultNotFoundError,
    )

    # 例外タイプとHTTP例外のマッピングを定義
    exception_mapping = {
        ValueError: lambda e: BadRequestError(str(e)),
        InvalidInputError: lambda e: BadRequestError(str(e)),
        DocumentProcessingError: lambda e: BadRequestError(str(e)),
        ResultNotFoundError: lambda e: NotFoundError(str(e)),
        VectorStoreOperationError: lambda e: InternalServerError(str(e)),
        RAGProcessingError: lambda e: InternalServerError(str(e)),
        SaveObjectToStorageError: lambda e: InternalServerError(str(e)),
    }

    # 例外タイプに基づいて適切なHTTP例外を返す
    for exc_type, handler in exception_mapping.items():
        if isinstance(exception, exc_type):
            return handler(exception)

    # マッピングにない例外はInternalServerErrorとして扱う
    return InternalServerError(f"Unexpected error: {str(exception)}")
