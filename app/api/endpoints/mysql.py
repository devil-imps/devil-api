from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from app.schemas.mysql import MySQLAccessAdd
from app.schemas.mysql import MySQLDbAdd
from app.schemas.mysql import MySQLPasswd
from app.schemas.mysql import MySQLPrivileges
from app.schemas.mysql import MySQLUserAdd
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/mysql", tags=["mysql"])


@router.post("/db/add", summary="Create MySQL database")
async def mysql_db_add(data: MySQLDbAdd):
    """
    Create a MySQL database (optionally set collation).

    Maps to: ``devil mysql db add database_name [--collate=...]``
    """
    args = ["--json", "mysql", "db", "add", data.database_name]
    if data.collate:
        args.append(data.collate)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql db add error: {exc}"
        ) from exc


@router.delete("/db/{database_name}", summary="Delete MySQL database")
async def mysql_db_del(
    database_name: str = Path(..., description="Name of the MySQL database to delete"),
):
    """
    Delete a MySQL database.

    Maps to: ``devil mysql db del database_name``.
    """
    args = ["--json", "mysql", "db", "del", database_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql db del error: {exc}"
        ) from exc


@router.post("/user/add", summary="Create MySQL user")
async def mysql_user_add(data: MySQLUserAdd):
    """
    Create a MySQL user.

    Maps to: ``devil mysql user add user_name`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "mysql", "user", "add", data.user_name]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql user add error: {exc}"
        ) from exc


@router.delete("/user/{user_name}", summary="Delete MySQL user")
async def mysql_user_del(
    user_name: str = Path(..., description="Name of the MySQL user to delete"),
):
    """
    Delete a MySQL user.

    Maps to: ``devil mysql user del user_name``.
    """
    args = ["--json", "mysql", "user", "del", user_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql user del error: {exc}"
        ) from exc


@router.post("/access/add", summary="Add MySQL host access")
async def mysql_access_add(data: MySQLAccessAdd):
    """
    Add host access for a MySQL user.

    Maps to: ``devil mysql access add user_name@host_name``.
    """
    args = ["--json", "mysql", "access", "add", f"{data.user_name}@{data.host_name}"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql access add error: {exc}"
        ) from exc


@router.delete("/access/{user_name}@{host_name}", summary="Remove MySQL host access")
async def mysql_access_del(
    user_name: str = Path(
        ..., description="Name of the MySQL user to remove access for"
    ),
    host_name: str = Path(..., description="Host name to remove access from"),
):
    """
    Remove host access for a MySQL user.

    Maps to: ``devil mysql access del user_name@host_name``.
    """
    args = ["--json", "mysql", "access", "del", f"{user_name}@{host_name}"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql access del error: {exc}"
        ) from exc


@router.put("/privileges", summary="Set MySQL privileges")
async def mysql_privileges(data: MySQLPrivileges):
    """
    Set privileges for a user (optionally host-qualified) on a database.

    Maps to: ``devil mysql privileges user_name[@host_name] database_name mysql_privileges``.
    """
    user_part = (
        data.user_name
        if data.host_name is None
        else f"{data.user_name}@{data.host_name}"
    )
    args = [
        "--json",
        "mysql",
        "privileges",
        user_part,
        data.database_name,
        ",".join(data.mysql_privileges),
    ]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"privileges error: {exc}") from exc


@router.put("/passwd", summary="Change MySQL password")
async def mysql_passwd(data: MySQLPasswd):
    """
    Change password for a MySQL user (optionally host-qualified).

    Maps to: ``devil mysql passwd user_name[@host_name]`` (interactive password supplied via API or generated randomly if not provided).
    """
    user_part = (
        data.user_name
        if data.host_name is None
        else f"{data.user_name}@{data.host_name}"
    )
    args = ["--json", "mysql", "passwd", user_part]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"mysql passwd error: {exc}"
        ) from exc


@router.get("/list", summary="List MySQL databases and users", tags=["read-only"])
async def mysql_list():
    """
    List MySQL databases and users.

    Maps to: ``devil mysql list -v|--verbose`` (always returning verbose output).
    """
    args = ["--json", "mysql", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"mysql list error: {exc}") from exc
