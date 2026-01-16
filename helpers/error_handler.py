from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from helpers.response import api_response
from helpers.i18n import get_message
from app_logging.logger import setup_logger
from slowapi.errors import RateLimitExceeded


logger = setup_logger()


def http_exception_handler(request: Request, exc: HTTPException):
     
    logger.error(
        "unhandled_exception",
        extra={
            "event": "unhandled_exception",
            "error_code": "INTERNAL_ERROR"
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=api_response(
            status="error",
            message=exc.detail,
            meta={"error_code": "HTTP_ERROR"}
        )
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
     
    logger.error(
        "unhandled_exception",
        extra={
            "event": "unhandled_exception",
            "error_code": "INTERNAL_ERROR"
        }
    )

    return JSONResponse(
        status_code=422,
        content=api_response(
            status="error",
            message=get_message("internal_error", "en"),
            meta={
                "error_code": "VALIDATION_ERROR",
                "details": exc.errors()
            }
        )
    )


def general_exception_handler(request: Request, exc: Exception):
    
    logger.error(
        "unhandled_exception",
        extra={
            "event": "unhandled_exception",
            "error_code": "INTERNAL_ERROR"
        }
    )

    # ⚠️ Jangan bocorkan detail error ke user
    return JSONResponse(
        status_code=500,
        content=api_response(
            status="error",
            message=get_message("internal_error", "en"),
            meta={"error_code": "INTERNAL_ERROR"}
        )
    )

def rate_limit_exception_handler(request, exc: RateLimitExceeded):
     # ✅ INILAH TEMPAT LOGGING RATE LIMIT
    logger.warning(
        "rate_limit_exceeded",
        extra={
            "event": "rate_limit_exceeded",
            "status": "blocked",
            "client_ip": request.client.host if request.client else None,
            "path": request.url.path
        }
    )
    
    return JSONResponse(
        status_code=429,
        content=api_response(
            status="error",
            message="Too many requests",
            meta={
                "error_code": "RATE_LIMIT_EXCEEDED"
            }
        )
    )
