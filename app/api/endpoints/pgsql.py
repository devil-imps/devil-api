from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from app.schemas.pgsql import PgSQLDbAdd
from app.schemas.pgsql import PgSQLExtension
from app.schemas.pgsql import PgSQLPasswd
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/pgsql", tags=["pgsql"])


@router.post("/db/add", summary="Create PostgreSQL database")
async def pgsql_db_add(data: PgSQLDbAdd):
    """
    Create a PostgreSQL database (user with same name auto-created) with optional collation.

    Maps to: ``devil pgsql db add database_name [--collate=...]`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "pgsql", "db", "add", data.database_name]
    if data.password:
        args.append(data.password)
    else:
        args.append("")  # Generate password
    if data.collate:
        args.append(data.collate)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/db/{database_name}", summary="Delete PostgreSQL database")
async def pgsql_db_del(
    database_name: str = Path(
        ..., description="Name of the PostgreSQL database to delete"
    ),
):
    """
    Delete a PostgreSQL database.

    Maps to: ``devil pgsql db del database_name``.
    """
    args = ["--json", "pgsql", "db", "del", database_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/passwd", summary="Change PostgreSQL password")
async def pgsql_passwd(data: PgSQLPasswd):
    """
    Change PostgreSQL user password.

    Maps to: ``devil pgsql passwd user_name`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "pgsql", "passwd", data.user_name]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/extensions", summary="Enable PostgreSQL extension")
async def pgsql_extensions(data: PgSQLExtension):
    """
    Enable an extension for a PostgreSQL database.

    Maps to: ``devil pgsql extensions database_name extension``.
    """
    args = ["--json", "pgsql", "extensions", data.database_name, data.extension]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/list", summary="List PostgreSQL databases and users", tags=["read-only"])
async def pgsql_list():
    """
    List PostgreSQL databases and users.

    Maps to: ``devil pgsql list``.
    """
    args = ["--json", "pgsql", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
