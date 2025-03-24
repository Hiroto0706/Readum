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

    if isinstance(exception, ValueError):
        return BadRequestError(str(exception))
    elif isinstance(exception, InvalidInputError):
        return BadRequestError(str(exception))
    elif isinstance(exception, DocumentProcessingError):
        return BadRequestError(str(exception))
    elif isinstance(exception, VectorStoreOperationError):
        return InternalServerError(str(exception))
    elif isinstance(exception, RAGProcessingError):
        return InternalServerError(str(exception))
    else:
        return InternalServerError(f"Unexpected error: {str(exception)}")
