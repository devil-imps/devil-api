from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from app.schemas.www import WWWAdd
from app.schemas.www import WWWDel
from app.schemas.www import WWWOptions
from app.schemas.www import WWWStatsAccessAdd
from app.schemas.www import WWWStatsAccessDel
from app.schemas.www import WWWStatsAccountAdd
from app.schemas.www import WWWStatsAccountDel
from app.schemas.www import WWWStatsAccountPasswd
from app.schemas.www import WWWStatsDomainAdd
from app.schemas.www import WWWStatsDomainDel
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/www", tags=["www"])


@router.post("/add", summary="Add website")
async def www_add(data: WWWAdd):
    """
    Add a website (standard, pointer, proxy, or passenger app).

    Maps to the family of commands:
        - ``devil www add www_domain [www_type]`` (php or basic types)
        - ``devil www add www_domain pointer pointer_target``
        - ``devil www add www_domain proxy proxy_target proxy_port``
        - ``devil www add www_domain python|nodejs|ruby passenger_binary www_environment``

    Logic selects variant based on provided fields. Exactly one variant must match.
    """
    args = ["--json", "www", "add", data.www_domain]
    # choose variant based on provided fields
    if data.pointer_target:
        args.extend(["pointer", data.pointer_target])
    elif data.proxy_target and data.proxy_port:
        args.extend(["proxy", data.proxy_target, str(data.proxy_port)])
    elif (
        data.passenger_binary
        and data.www_environment
        and data.www_type in {"python", "nodejs", "ruby"}
    ):
        args.extend([data.www_type, data.passenger_binary, data.www_environment])
    elif data.www_type:
        args.append(data.www_type)
    else:
        args.append("php")
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/del/{www_domain}", summary="Delete website")
async def www_del(data: WWWDel):
    """
    Delete a website (optionally removing data).

    Maps to: ``devil www del www_domain [--remove]``.
    """
    args = ["--json", "www", "del", data.www_domain]
    if data.remove:
        args.append("--remove")
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# TODO: Add validation for option values
@router.put("/options", summary="Change website option")
async def www_options(data: WWWOptions):
    """
    Change website option.

    Maps to: ``devil www options www_domain www_option value`` (value semantic depends on option).
    """
    args = ["--json", "www", "options", data.www_domain, data.www_option, data.value]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/restart/{www_domain}", summary="Restart passenger app")
async def www_restart(www_domain: str = Path(..., description="Website domain")):
    """
    Restart a passenger hosted app (python/node/ruby).

    Maps to: ``devil www restart www_domain``.
    """
    args = ["--json", "www", "restart", www_domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/list", summary="List websites")
async def www_list():
    """List websites.

    Maps to: ``devil www list -v|--verbose`` (always returning verbose output).
    """
    args = ["--json", "www", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/stats/account/add", summary="Add stats account")
async def www_stats_account_add(data: WWWStatsAccountAdd):
    """
    Create a Matomo stats account.

    Maps to: ``devil www stats account add user_name`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "www", "stats", "account", "add", data.user_name]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/stats/account/{user_name}", summary="Delete stats account")
async def www_stats_account_del(data: WWWStatsAccountDel):
    """
    Delete a Matomo stats account.

    Maps to: ``devil www stats account del user_name``.
    """
    args = ["--json", "www", "stats", "account", "del", data.user_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/stats/account/passwd", summary="Change stats account password")
async def www_stats_account_passwd(data: WWWStatsAccountPasswd):
    """
    Change password for a Matomo stats account.

    Maps to: ``devil www stats account passwd user_name`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = [
        "--json",
        "www",
        "stats",
        "account",
        "passwd",
        data.user_name,
    ]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/stats/access/add", summary="Grant stats access")
async def www_stats_access_add(data: WWWStatsAccessAdd):
    """
    Grant Matomo stats access for a website to a stats user.

    Maps to: ``devil www stats access add www_domain user_name``.
    """
    args = ["--json", "www", "stats", "access", "add", data.www_domain, data.user_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/stats/access/{www_domain}/{user_name}", summary="Revoke stats access")
async def www_stats_access_del(data: WWWStatsAccessDel):
    """
    Revoke Matomo stats access.

    Maps to: ``devil www stats access del www_domain user_name``.
    """
    args = ["--json", "www", "stats", "access", "del", data.www_domain, data.user_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/stats/domain/add", summary="Add stats domain")
async def www_stats_domain_add(data: WWWStatsDomainAdd):
    """
    Add a domain to Matomo stats tracking.

    Maps to: ``devil www stats domain add www_domain``.
    """
    args = ["--json", "www", "stats", "domain", "add", data.www_domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/stats/domain/{www_domain}", summary="Delete stats domain")
async def www_stats_domain_del(data: WWWStatsDomainDel):
    """
    Remove a domain from Matomo stats tracking.

    Maps to: ``devil www stats domain del www_domain``.
    """
    args = ["--json", "www", "stats", "domain", "del", data.www_domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/stats/list", summary="List stats users/domains")
async def www_stats_list():
    """
    List Matomo stats users and domains.

    Maps to: ``devil www stats list``.
    """
    args = ["--json", "www", "stats", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
