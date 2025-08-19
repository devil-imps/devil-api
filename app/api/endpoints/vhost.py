from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query

from app.schemas.vhost import VHostType
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/vhost", tags=["vhost"])


@router.get("/list", summary="List IP addresses", tags=["read-only"])
async def vhost_list(
    vhost_type: VHostType | None = Query(
        None, description="Vhost type: private, public or all"
    ),
):
    """
    List available IP addresses.

    Maps to: ``devil vhost list [vhost_type]`` where vhost_type ∈ {private, public, all}.
    """
    args = ["--json", "vhost", "list"]
    if vhost_type:
        args.append(vhost_type)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
