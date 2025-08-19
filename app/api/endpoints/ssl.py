from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query

from app.schemas.ssl import SSLMailAdd
from app.schemas.ssl import SSLMailGet
from app.schemas.ssl import SSLWWWAdd
from app.schemas.ssl import SSLWWWGet
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/ssl", tags=["ssl"])


@router.post("/www/add", summary="Add WWW SSL certificate")
async def ssl_www_add(data: SSLWWWAdd):
    """
    Add a WWW SSL certificate (standard or Let's Encrypt).

    Maps to:
      - ``devil ssl www add ssl_ip ssl_cert_file ssl_key_file [domain]``
      - ``devil ssl www add ssl_ip le le domain`` (when le=true)
    Provide domain when using SNI or Let's Encrypt.
    """
    args = ["--json", "ssl", "www", "add", data.ssl_ip]
    if data.le:
        args.extend(["le", "le"])
        if not data.domain:
            raise HTTPException(
                status_code=400, detail="domain required for Let's Encrypt"
            )
        args.append(data.domain)
    else:
        if not (data.ssl_cert_file and data.ssl_key_file):
            raise HTTPException(
                status_code=400,
                detail="ssl_cert_file and ssl_key_file required unless le=true",
            )
        args.extend([data.ssl_cert_file, data.ssl_key_file])
        if data.domain:
            args.append(data.domain)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/www/{ssl_ip}", summary="Delete WWW SSL certificate")
async def ssl_www_del(
    ssl_ip: str = Path(..., description="SSL IP address"),
    domain: str | None = Query(None, description="Optional SNI domain"),
):
    """
    Delete a WWW SSL certificate (optionally SNI domain).

    Maps to: ``devil ssl www del ssl_ip [domain]``.
    """
    args = ["--json", "ssl", "www", "del", ssl_ip]
    if domain:
        args.append(domain)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/www/get", summary="Get WWW SSL certificate", tags=["read-only"])
async def ssl_www_get(data: SSLWWWGet):
    """
    Get certificate and key for a WWW SSL entry.

    Maps to: ``devil ssl www get ssl_ip [domain]``.
    """
    args = ["--json", "ssl", "www", "get", data.ssl_ip]
    if data.domain:
        args.append(data.domain)
    args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/www/list", summary="List WWW SSL certificates", tags=["read-only"])
async def ssl_www_list():
    """
    List all WWW SSL certificates.

    Maps to: ``devil ssl www list``.
    """
    args = ["--json", "ssl", "www", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/mail/add", summary="Add mail SSL certificate")
async def ssl_mail_add(data: SSLMailAdd):
    """
    Add a mail SSL certificate.

    Maps to: ``devil ssl mail add ssl_ip ssl_cert_file ssl_key_file``.
    """
    args = [
        "--json",
        "ssl",
        "mail",
        "add",
        data.ssl_ip,
        data.ssl_cert_file,
        data.ssl_key_file,
    ]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/mail/{ssl_ip}", summary="Delete mail SSL certificate")
async def ssl_mail_del(ssl_ip: str = Path(..., description="SSL IP address")):
    """
    Delete a mail SSL certificate.

    Maps to: ``devil ssl mail del ssl_ip``.
    """
    args = ["--json", "ssl", "mail", "del", ssl_ip]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/mail/get", summary="Get mail SSL certificate", tags=["read-only"])
async def ssl_mail_get(data: SSLMailGet):
    """
    Get certificate and key for a mail SSL entry.

    Maps to: ``devil ssl mail get ssl_ip``.
    """
    args = ["--json", "ssl", "mail", "get", data.ssl_ip, data.password]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/mail/list", summary="List mail SSL certificates", tags=["read-only"])
async def ssl_mail_list():
    """
    List all mail SSL certificates.

    Maps to: ``devil ssl mail list``.
    """
    args = ["--json", "ssl", "mail", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
