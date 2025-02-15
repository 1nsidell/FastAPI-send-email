"""Модуль обработчика ошибок"""

import logging
from core.exceptions import BaseCustomException
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

log = logging.getLogger("exception_handler")


def custom_exception_handler(request: Request, exc: BaseCustomException):
    """Создание обработкчика кастомных ошибок"""
    error_data = {"error_type": exc.error_type, "message": exc.message}
    log.warning(f"Custom Exception occurred: {error_data} | Path: {request.url}")
    return JSONResponse(content=error_data, status_code=exc.status_code)


async def general_exception_handler(request: Request, exc: Exception):
    """Создание обработкчика непредвиденных ошибок"""
    error_data = {
        "error_type": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred.",
    }
    log.exception(f"General Exception occurred: {exc} | Path: {request.url}")
    return JSONResponse(content=error_data, status_code=500)


def apply_exceptions_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    return app
