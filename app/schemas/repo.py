from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field

__all__ = [
    "RepoAccountAdd",
    "RepoAccountPasswd",
    "RepoRepositoryAdd",
    "RepoRepositoryChange",
    "RepoType",
    "RepoVisibility",
]


class RepoType(str, Enum):
    git = "git"
    svn = "svn"
    hg = "hg"


class RepoVisibility(str, Enum):
    pub = "pub"
    priv = "priv"


class RepoRepositoryAdd(BaseModel):
    repo_type: RepoType = Field(..., description="git, svn or hg")
    repo_name: str = Field(..., description="Repository name")
    repo_visibility: RepoVisibility = Field(..., description="pub or priv")


class RepoRepositoryChange(BaseModel):
    repo_type: RepoType = Field(..., description="Repository type: git, svn or hg")
    repo_name: str = Field(..., description="Repository name")
    repo_visibility: RepoVisibility = Field(
        ..., description="Target visibility: pub or priv"
    )


class RepoAccountAdd(BaseModel):
    repo_type: RepoType = Field(..., description="Repository type")
    repo_name: str = Field(..., description="Repository name")
    repo_username: str = Field(..., description="Account username to add")
    password: str | None = Field(
        None,
        description="Optional password when creating account, generated randomly if not provided",
    )


class RepoAccountPasswd(BaseModel):
    repo_type: RepoType = Field(..., description="Repository type")
    repo_name: str = Field(..., description="Repository name")
    repo_username: str = Field(
        ..., description="Account username whose password changes"
    )
    password: str | None = Field(
        None, description="New password, generated randomly if not provided"
    )
