from fastapi import Request, status
from fastapi.responses import JSONResponse


async def unhandled_exception_handler(
    request: Request, error: Exception
) -> JSONResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    error_message = (
        "Unhandled error" if str(error).__contains__("sqlalchemy") else str(error)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": {
                "code": "UNHANDLED_ERROR",
                "message": error_message,
            }
        },
    )
