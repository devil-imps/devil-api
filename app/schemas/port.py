from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field

__all__ = ["PortAdd", "PortType"]


class PortType(str, Enum):
    tcp = "tcp"
    udp = "udp"


class PortAdd(BaseModel):
    type: PortType = Field(..., description="Port type: tcp or udp")
    port: int | None = Field(None, description="Specific port number")
    random: bool = Field(False, description="Request random available port")
    description: str | None = Field(None, description="Description for reservation")
