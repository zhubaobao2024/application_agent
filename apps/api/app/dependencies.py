"""
Common FastAPI dependencies.
"""
from typing import Optional, Dict, Any
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.core.cache import get_cache, Cache
from app.core.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    AuthenticationException
)

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Verify JWT token and return current user data.

    Args:
        credentials: Bearer token credentials

    Returns:
        User data from token payload

    Raises:
        InvalidTokenException: If token is invalid
        TokenExpiredException: If token has expired
    """
    token = credentials.credentials

    # Verify and decode token
    payload = verify_token(token)

    if payload is None:
        raise InvalidTokenException()

    # Check if token has expired
    if "exp" not in payload:
        raise InvalidTokenException()

    # Extract user ID
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenException()

    return {
        "id": user_id,
        "email": payload.get("email"),
        **payload
    }


async def get_optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[Dict[str, Any]]:
    """
    Get current user if token is provided, otherwise return None.
    Useful for endpoints that work with or without authentication.

    Args:
        authorization: Authorization header value

    Returns:
        User data if authenticated, None otherwise
    """
    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if payload is None:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    return {
        "id": user_id,
        "email": payload.get("email"),
        **payload
    }


def get_db_session() -> Session:
    """
    Get database session.
    Alias for get_db for clearer naming in route dependencies.
    """
    return Depends(get_db)


def get_cache_instance() -> Cache:
    """
    Get cache instance.
    """
    return Depends(get_cache)
