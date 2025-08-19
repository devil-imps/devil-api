from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/info", tags=["info"])


@router.get("/limits", summary="Account limits", tags=["read-only"])
async def info_limits():
    """
    Return account limits information.

    Maps to: ``devil info limits``.
    """
    try:
        return await execute_devil_command(["--json", "info", "limits"])
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/account", summary="Basic account info", tags=["read-only"])
async def info_account():
    """
    Return basic account information.

    Maps to: ``devil info account``.
    """
    try:
        return await execute_devil_command(["--json", "info", "account"])
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
