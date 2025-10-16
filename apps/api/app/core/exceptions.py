"""
Custom exception classes for the application.
"""
from typing import Optional, Any, Dict
from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base exception for application-specific errors."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


# Authentication Exceptions
class AuthenticationException(AppException):
    """Base authentication exception."""
    def __init__(self, detail: str = "Authentication failed", error_code: str = "AUTH_FAILED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsException(AuthenticationException):
    """Invalid email or password."""
    def __init__(self):
        super().__init__(
            detail="Invalid email or password",
            error_code="AUTH_INVALID_CREDENTIALS"
        )


class TokenExpiredException(AuthenticationException):
    """JWT token has expired."""
    def __init__(self):
        super().__init__(
            detail="Token has expired",
            error_code="AUTH_TOKEN_EXPIRED"
        )


class InvalidTokenException(AuthenticationException):
    """Invalid JWT token."""
    def __init__(self):
        super().__init__(
            detail="Invalid token",
            error_code="AUTH_TOKEN_INVALID"
        )


class InsufficientPermissionsException(AppException):
    """User lacks required permissions."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
            error_code="AUTH_INSUFFICIENT_PERMISSIONS"
        )


# Resource Exceptions
class ResourceNotFoundException(AppException):
    """Requested resource not found."""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
            error_code="RESOURCE_NOT_FOUND"
        )


class ResourceAlreadyExistsException(AppException):
    """Resource already exists."""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists",
            error_code="RESOURCE_ALREADY_EXISTS"
        )


# Validation Exceptions
class ValidationException(AppException):
    """Input validation failed."""
    def __init__(self, detail: str, field: Optional[str] = None):
        error_detail = detail
        if field:
            error_detail = f"{field}: {detail}"

        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_detail,
            error_code="VALIDATION_FAILED"
        )


class RequiredFieldException(ValidationException):
    """Required field is missing."""
    def __init__(self, field: str):
        super().__init__(
            detail="This field is required",
            field=field
        )


# Rate Limiting Exception
class RateLimitException(AppException):
    """Rate limit exceeded."""
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Retry after {retry_after} seconds",
            error_code="RATE_LIMIT_EXCEEDED",
            headers={"Retry-After": str(retry_after)}
        )


# External Service Exceptions
class ExternalServiceException(AppException):
    """External service error."""
    def __init__(self, service: str, detail: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{service} error: {detail}",
            error_code=f"{service.upper()}_SERVICE_ERROR"
        )


class AIServiceException(ExternalServiceException):
    """AI provider error."""
    def __init__(self, detail: str = "AI service error"):
        super().__init__(service="AI", detail=detail)


class AIServiceTimeoutException(AppException):
    """AI generation timed out."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI generation timed out",
            error_code="AI_SERVICE_TIMEOUT"
        )


class ScraperException(ExternalServiceException):
    """Job scraping error."""
    def __init__(self, detail: str = "Scraping failed"):
        super().__init__(service="Scraper", detail=detail)


class StorageException(ExternalServiceException):
    """File storage error."""
    def __init__(self, detail: str = "Storage operation failed"):
        super().__init__(service="Storage", detail=detail)
