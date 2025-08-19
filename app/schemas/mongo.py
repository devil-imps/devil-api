from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

__all__ = ["MongoDbAdd", "MongoPasswd"]


class MongoDbAdd(BaseModel):
    database_name: str = Field(..., description="Database name")
    password: str | None = Field(
        None,
        description="Password for auto-created user, generated randomly if not provided",
    )


class MongoPasswd(BaseModel):
    user_name: str = Field(..., description="MongoDB user name")
    password: str | None = Field(
        None, description="New password, generated randomly if not provided"
    )
