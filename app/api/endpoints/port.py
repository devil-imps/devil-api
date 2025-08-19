from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path

from app.schemas.port import PortAdd
from app.schemas.port import PortType
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/port", tags=["port"])


@router.post("/add", summary="Reserve port (or random)")
async def port_add(data: PortAdd):
    """
    Reserve a TCP/UDP port (or get a random one).

    Maps to: ``devil port add type port [description]`` or ``devil port add type random [description]``.
    Constraints: Provide either random=true or a concrete port value.
    """
    args = ["--json", "port", "add", data.type]
    if data.random and data.port:
        raise HTTPException(
            status_code=400, detail="Provide either random or port, not both"
        )
    if data.random:
        args.append("random")
    elif data.port is not None:
        args.append(str(data.port))
    else:
        raise HTTPException(status_code=400, detail="Provide port or set random=true")
    if data.description:
        args.append(data.description)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{type}/{port}", summary="Release reserved port")
async def port_del(
    type: PortType = Path(..., description="Port type: tcp or udp"),
    port: int = Path(..., description="Port number to release"),
):
    """
    Release a reserved port.

    Maps to: ``devil port del type port``.
    """
    args = ["--json", "port", "del", type, str(port)]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/list", summary="List reserved ports", tags=["read-only"])
async def port_list():
    """
    List all reserved ports.

    Maps to: ``devil port list``.
    """
    args = ["--json", "port", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
