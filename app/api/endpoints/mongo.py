from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from app.schemas.mongo import MongoDbAdd
from app.schemas.mongo import MongoPasswd
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/mongo", tags=["mongo"])


@router.post("/db/add", summary="Create MongoDB database")
async def mongo_db_add(data: MongoDbAdd):
    """
    Create a MongoDB database (and user with same name) with supplied password.

    Maps to: ``devil mongo db add database_name`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "mongo", "db", "add", data.database_name]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/db/{database_name}", summary="Delete MongoDB database")
async def mongo_db_del(
    database_name: str = Path(
        ..., description="Name of the MongoDB database to delete"
    ),
):
    """
    Delete a MongoDB database.

    Maps to: ``devil mongo db del database_name``.
    """
    args = ["--json", "mongo", "db", "del", database_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/passwd", summary="Change MongoDB password")
async def mongo_passwd(data: MongoPasswd):
    """
    Change MongoDB user password.

    Maps to: ``devil mongo passwd user_name`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "mongo", "passwd", data.user_name]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/list", summary="List MongoDB databases and users")
async def mongo_list():
    """
    List MongoDB databases and users.

    Maps to: ``devil mongo list``.
    """
    args = ["--json", "mongo", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
