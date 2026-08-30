"""
Centralized error handling for the Personalized Learning Path Recommender.

Provides:
- A structured error response shape for all API errors.
- FastAPI exception handlers that normalize 4xx/5xx responses.
- The AIUnavailableError raised when the Gemini service is not configured or fails,
  along with graceful fallback handling so the API never hard-crashes.
"""
from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Any, Dict, Optional


class ErrorResponse(BaseModel):
    """Standard error payload returned by every API failure."""
    error: str
    message: str
    detail: Optional[Dict[str, Any]] = None


class AIUnavailableError(Exception):
    """Raised when the Gemini LLM/embedding service is unavailable or unconfigured.

    The API layer catches this and returns a 503 with a helpful message instead of
    a generic 500, and AI-dependent endpoints degrade to fallback behaviour.
    """


class CourseNotFoundError(Exception):
    """Raised when a referenced course/skill cannot be resolved to a resource."""


def _error(error: str, message: str, status_code: int, detail: Any = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(error=error, message=message, detail=detail).model_dump(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register normalized exception handlers on a FastAPI application."""

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(request: Request, exc: RequestValidationError):
        # Return a structured 422 with the list of field errors so the frontend
        # can render actionable messages next to each field.
        return _error(
            error="validation_error",
            message="The request was invalid. Please check the highlighted fields.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": exc.errors()},
        )

    @app.exception_handler(AIUnavailableError)
    async def _ai_unavailable_handler(request: Request, exc: AIUnavailableError):
        return _error(
            error="ai_unavailable",
            message="The AI service is temporarily unavailable. Your progress was still saved; please try again in a moment.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"reason": str(exc) or "gemini service unavailable"},
        )

    @app.exception_handler(CourseNotFoundError)
    async def _course_not_found_handler(request: Request, exc: CourseNotFoundError):
        return _error(
            error="course_not_found",
            message="We couldn't find a suitable course for that skill.",
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"reason": str(exc)},
        )

    @app.exception_handler(ValueError)
    async def _value_error_handler(request: Request, exc: ValueError):
        return _error(
            error="bad_request",
            message=str(exc) or "Invalid request data.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(Exception)
    async def _unhandled_exception_handler(request: Request, exc: Exception):
        # Catch-all: never leak stack traces to clients; return a clean 500.
        # The full traceback is logged by uvicorn for debugging server-side.
        print(f"[error] Unhandled exception on {request.method} {request.url.path}: {exc!r}")
        return _error(
            error="internal_error",
            message="Something went wrong on our side. Please try again, or contact support if the problem persists.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
