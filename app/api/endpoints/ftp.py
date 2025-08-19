from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from fastapi import status

from app.schemas.ftp import FTPAdd
from app.schemas.ftp import FTPPasswd
from app.schemas.ftp import FTPQuota
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/ftp", tags=["ftp"])


@router.post("/add", summary="Create FTP account")
async def ftp_add(data: FTPAdd):
    """
    Create an FTP account.

    Maps to: ``devil ftp add ftp_username ftp_directory ftp_quota`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = [
        "--json",
        "ftp",
        "add",
        data.username,
        data.directory,
        data.quota,
    ]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/{username}", summary="Delete FTP account")
async def ftp_del(
    username: str = Path(..., description="FTP account username to delete"),
):
    """
    Remove an FTP account.

    Maps to: ``devil ftp del ftp_username``.
    """
    args = ["--json", "ftp", "del", username]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.put("/passwd", summary="Change FTP password")
async def ftp_passwd(data: FTPPasswd):
    """
    Change FTP account password.

    Maps to: ``devil ftp passwd ftp_username`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "ftp", "passwd", data.username]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.put("/quota", summary="Change FTP quota or recalc")
async def ftp_quota(data: FTPQuota):
    """
    Change or recalc FTP quota.

    Maps to: ``devil ftp quota ftp_username ftp_quota|recalc``.
    """
    args = ["--json", "ftp", "quota", data.username, data.quota]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/list", summary="List FTP accounts", tags=["read-only"])
async def ftp_list():
    """
    List all FTP accounts.

    Maps to: ``devil ftp list``.
    """
    args = ["--json", "ftp", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
