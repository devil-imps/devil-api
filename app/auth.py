from __future__ import annotations

import logging
import os
import time

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi import Request
from fastapi import Security
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi.security.api_key import APIKeyHeader

load_dotenv()

logger = logging.getLogger(__name__)

expected_api_key = os.getenv("DEVIL_API_KEY")
if not expected_api_key:
    raise RuntimeError(
        "DEVIL_API_KEY environment variable must be set before starting the API server"
    )

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
BearerScheme = HTTPBearer(auto_error=False)

AUTH_FAILURE_TRACKER: dict[str, dict[str, float | int]] = {}
AUTH_FAIL_THRESHOLD = int(os.getenv("DEVIL_AUTH_FAIL_THRESHOLD", "5"))
AUTH_BLOCK_SECONDS = int(os.getenv("DEVIL_AUTH_BLOCK_SECONDS", "300"))


def _client_ip(request: Request) -> str:
    """
    Extract client IP address from FastAPI request.
    If behind a proxy, this does not use X-Forwarded-For.
    """
    return request.client.host if request.client else "unknown"


def _register_auth_failure(ip: str) -> tuple[bool, float]:
    """
    Register a failed authentication attempt for the given IP.
    Returns (blocked: bool, blocked_until: float).
    If threshold is reached, sets block timer.
    """
    now = time.time()
    rec = AUTH_FAILURE_TRACKER.get(ip)
    if rec is None:
        rec = {"fail_count": 1, "first_fail_ts": now, "blocked_until": 0.0}
        AUTH_FAILURE_TRACKER[ip] = rec
    else:
        if rec.get("blocked_until", 0.0) and now >= rec["blocked_until"]:
            rec["fail_count"] = 0
            rec["blocked_until"] = 0.0
            rec["first_fail_ts"] = now
        rec["fail_count"] = int(rec.get("fail_count", 0)) + 1
    if rec["fail_count"] >= AUTH_FAIL_THRESHOLD:
        rec["blocked_until"] = now + AUTH_BLOCK_SECONDS
        return True, rec["blocked_until"]
    return False, 0.0


def _is_blocked(ip: str) -> bool:
    """
    Check if the given IP is currently blocked due to repeated auth failures.
    Returns True if blocked, False otherwise.
    """
    rec = AUTH_FAILURE_TRACKER.get(ip)
    if not rec:
        return False
    blocked_until = rec.get("blocked_until", 0.0) or 0.0
    now = time.time()
    if blocked_until and now < blocked_until:
        return True
    if blocked_until and now >= blocked_until:
        rec["blocked_until"] = 0.0
        rec["fail_count"] = 0
    return False


async def verify_api_key(
    request: Request,
    x_api_key: str | None = Security(api_key_header),
    bearer: HTTPAuthorizationCredentials | None = Security(BearerScheme),
) -> None:
    """
    FastAPI dependency for API authentication.
    Accepts either X-API-Key header or Authorization: Bearer token.
    Applies per-IP rate limiting and logs failures.
    Raises HTTP 401 for auth errors, 429 for rate limit blocks.
    """
    ip = _client_ip(request)
    if _is_blocked(ip):
        logger.warning("Auth attempt while blocked ip=%s", ip)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed authentication attempts",
        )
    supplied = x_api_key or (
        bearer.credentials if bearer and bearer.scheme.lower() == "bearer" else None
    )
    if not supplied or supplied != expected_api_key:
        blocked, until = _register_auth_failure(ip)
        logger.warning(
            "Authentication failed ip=%s fail_count=%s blocked=%s until=%s",
            ip,
            AUTH_FAILURE_TRACKER.get(ip, {}).get("fail_count"),
            blocked,
            int(until) if until else 0,
        )
        if blocked:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed authentication attempts",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    rec = AUTH_FAILURE_TRACKER.get(ip)
    if rec:
        rec["fail_count"] = 0
        rec["blocked_until"] = 0.0


__all__ = [
    "AUTH_BLOCK_SECONDS",
    "AUTH_FAILURE_TRACKER",
    "AUTH_FAIL_THRESHOLD",
    "verify_api_key",
]
