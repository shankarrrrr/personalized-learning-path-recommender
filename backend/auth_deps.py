"""
FastAPI dependencies for authentication.

get_current_user: decodes the JWT from the Authorization header and returns
the User row, raising 401 for missing/invalid tokens.
get_current_user_optional: returns the User or None, so endpoints can behave
differently for authenticated vs anonymous users (e.g. scope analytics).
"""
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from services.auth_service import decode_access_token

# tokenUrl points at the login endpoint; used by Swagger UI's "Authorize" button.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """Require a valid JWT and return the authenticated user, else 401."""
    creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise creds_exc
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise creds_exc
    user_id = payload["sub"]
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise creds_exc
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.is_active:
        raise creds_exc
    return user


def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Return the authenticated user if a valid token is present, else None.

    Used by endpoints that support both anonymous and authenticated access.
    """
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()
