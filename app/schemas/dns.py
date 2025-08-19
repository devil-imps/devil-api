from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field

__all__ = ["DNSAddRecord", "DNSAddZone", "DNSDel"]


class DNSTypes(str, Enum):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    NS = "NS"
    SRV = "SRV"
    TXT = "TXT"
    CAA = "CAA"


class DNSAddZone(BaseModel):
    dns_domain: str = Field(..., description="Domain name to create zone for")
    dns_template: str | None = Field(
        None,
        description="Optional DNS template name to load (default is loaded automatically)",
    )


class DNSAddRecord(BaseModel):
    dns_domain: str = Field(..., description="Existing domain/zone name")
    dns_record: str = Field(..., description="Record name (relative or FQDN)")
    dns_record_type: DNSTypes = Field(
        ..., description="Record type: A, AAAA, CNAME, MX, NS, SRV, TXT, CAA"
    )
    dns_target: str = Field(..., description="Record target (ip, host, text)")
    ttl: int | None = Field(None, description="Optional TTL for the record")
    caa_tag: str | None = Field(
        None,
        description="CAA tag when dns_record_type=CAA (issue, issuewild, iodef, contactemail, contactphone)",
    )
    dns_prio: int | None = Field(
        None, description="Priority for MX/SRV when applicable"
    )
    dns_weight: int | None = Field(None, description="Weight for SRV when applicable")


class DNSDel(BaseModel):
    dns_domain: str = Field(
        ..., description="Domain whose zone or record should be deleted"
    )
    dns_record_id: int | None = Field(
        None,
        description=(
            "Optional record identifier. When omitted the whole zone is removed; when set only that record is deleted."
        ),
    )
