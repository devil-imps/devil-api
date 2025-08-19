from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

__all__ = ["FTPAdd", "FTPPasswd", "FTPQuota"]


class FTPAdd(BaseModel):
    username: str = Field(..., description="FTP account username")
    directory: str = Field(
        ...,
        description="Home directory path or relative path (must be under user home)",
    )
    quota: str = Field(..., description="Quota, e.g. 2G, 300M, recalc")
    password: str | None = Field(
        None,
        description="Plaintext password to set, generated randomly if not provided",
    )


class FTPPasswd(BaseModel):
    username: str = Field(
        ..., description="FTP username whose password will be changed"
    )
    password: str | None = Field(
        None, description="New plaintext password, generated randomly if not provided"
    )


class FTPQuota(BaseModel):
    username: str = Field(..., description="FTP username whose quota will be changed")
    quota: str = Field(
        ...,
        description="New quota (e.g. 2G, 300M) or the literal 'recalc' to recalculate usage",
    )
