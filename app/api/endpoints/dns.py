from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from app.schemas.dns import DNSAddRecord
from app.schemas.dns import DNSAddZone
from app.schemas.dns import DNSDel
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/dns", tags=["dns"])


@router.post("/add/zone", summary="Add DNS zone (load template)")
async def dns_add_zone(data: DNSAddZone):
    """
    Add a DNS zone for a domain, optionally loading a specific template.

    Maps to:
      - ``devil dns add dns_domain``
      - ``devil dns add dns_domain dns_template`` (DNS zone given domain must exist)
    """
    args = ["--json", "dns", "add", data.dns_domain]
    if data.dns_template:
        args.append(data.dns_template)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/add/record", summary="Add DNS record")
async def dns_add_record(data: DNSAddRecord):
    """
    Add a DNS record to an existing zone.

    Maps to variations of ``devil dns add dns_domain dns_record dns_record_type ...`` including CAA, MX/SRV with priority/weight and TTL.
    """
    args = [
        "--json",
        "dns",
        "add",
        data.dns_domain,
        data.dns_record,
        data.dns_record_type,
    ]

    t = data.dns_record_type.upper()
    # CAA requires additional caa_tag before target
    if t == "CAA":
        if not data.caa_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="caa_tag is required for CAA records",
            )
        if data.dns_prio is not None or data.dns_weight is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dns_prio/dns_weight not applicable to CAA",
            )
        args.extend([data.caa_tag, data.dns_target])
    # SRV may include prio and optionally weight
    elif t == "SRV":
        if data.dns_prio is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dns_prio is required for SRV records",
            )
        if data.dns_weight is not None:
            args.extend([str(data.dns_prio), str(data.dns_weight), data.dns_target])
        else:
            args.extend([str(data.dns_prio), data.dns_target])
        if data.caa_tag is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="caa_tag not applicable to SRV",
            )
    # MX requires priority
    elif t == "MX":
        if data.dns_prio is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dns_prio is required for MX records",
            )
        if data.dns_weight is not None or data.caa_tag is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dns_weight/caa_tag not applicable to MX",
            )
        args.extend([str(data.dns_prio), data.dns_target])
    else:
        # Generic case: just target
        if (
            data.dns_prio is not None
            or data.dns_weight is not None
            or data.caa_tag is not None
        ):
            # Validate combinations to avoid sending wrong shape
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dns_prio/dns_weight/caa_tag not applicable to this record type",
            )
        args.append(data.dns_target)

    if data.ttl is not None:
        args.append(str(data.ttl))

    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/templates", summary="List DNS templates", tags=["read-only"])
async def dns_templates():
    """
    List available DNS templates.

    Maps to: ``devil dns templates``.
    """
    try:
        return await execute_devil_command(["--json", "dns", "templates"])
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/list", summary="List DNS zones or records", tags=["read-only"])
async def dns_list(
    dns_domain: str | None = Query(
        None,
        description="Optional domain name. When supplied, returns records for that domain; when omitted, returns all zones.",
    ),
):
    """
    List DNS zones or records for a specific domain.

    Maps to: ``devil dns list [dns_domain]``.
    """
    args = ["--json", "dns", "list"]
    if dns_domain:
        args.append(dns_domain)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/del", summary="Delete DNS zone or record")
async def dns_del(data: DNSDel):
    """
    Delete a DNS zone or a specific record.

    Maps to: ``devil dns del dns_domain [dns_record_id]``.
    """
    args = ["--json", "dns", "del", data.dns_domain]
    if data.dns_record_id is not None:
        args.append(str(data.dns_record_id))
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
