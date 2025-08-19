from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

__all__ = [
    "SSLMailAdd",
    "SSLMailDel",
    "SSLMailGet",
    "SSLWWWAdd",
    "SSLWWWDel",
    "SSLWWWGet",
]


class SSLWWWAdd(BaseModel):
    ssl_ip: str = Field(..., description="User private or web server IP")
    ssl_cert_file: str | None = Field(None, description="Certificate file path")
    ssl_key_file: str | None = Field(None, description="Key file path")
    domain: str | None = Field(None, description="SNI domain")
    le: bool = Field(False, description="Use Let's Encrypt")


class SSLWWWDel(BaseModel):
    ssl_ip: str = Field(..., description="User private or web server IP")
    domain: str | None = Field(
        None, description="Optional SNI domain whose certificate should be removed"
    )


class SSLWWWGet(BaseModel):
    ssl_ip: str = Field(..., description="User private or web server IP")
    password: str = Field(..., description="devil account password")
    domain: str | None = Field(None, description="Optional SNI domain to fetch")


class SSLMailAdd(BaseModel):
    ssl_ip: str = Field(..., description="User private IP")
    ssl_cert_file: str = Field(..., description="Certificate file path")
    ssl_key_file: str = Field(..., description="Key file path matching certificate")


class SSLMailDel(BaseModel):
    ssl_ip: str = Field(..., description="User private IP whose mail cert is removed")


class SSLMailGet(BaseModel):
    ssl_ip: str = Field(..., description="User private IP whose mail cert is fetched")
    password: str = Field(..., description="devil account password")
