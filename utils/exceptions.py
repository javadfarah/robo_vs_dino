from fastapi import Request
from fastapi.responses import JSONResponse

__all__ = ['UnicornException', 'unicorn_exception_handler']


class UnicornException(Exception):
    def __init__(self, message: str, status_code):
        self.message = message
        self.status_code = status_code


async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
