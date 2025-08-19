from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query

from app.schemas.repo import RepoAccountAdd
from app.schemas.repo import RepoAccountPasswd
from app.schemas.repo import RepoRepositoryAdd
from app.schemas.repo import RepoRepositoryChange
from app.schemas.repo import RepoType
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/repo", tags=["repo"])


@router.post("/repository/add", summary="Create repository")
async def repo_repository_add(data: RepoRepositoryAdd):
    """
    Create a repository.

    Maps to: ``devil repo repository add repo_type repo_name repo_visibility``.
    Visibility: pub | priv.
    """
    if data.repo_visibility is None:
        raise HTTPException(status_code=400, detail="repo_visibility required")
    args = [
        "--json",
        "repo",
        "repository",
        "add",
        data.repo_type,
        data.repo_name,
        data.repo_visibility,
    ]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/repository/{repo_type}/{repo_name}", summary="Delete repository")
async def repo_repository_del(
    repo_type: RepoType = Path(..., description="Repository type: pub or priv"),
    repo_name: str = Path(..., description="Repository name"),
):
    """
    Delete a repository.

    Maps to: ``devil repo repository del repo_type repo_name``.
    """
    args = ["--json", "repo", "repository", "del", repo_type, repo_name]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/repository/change", summary="Change repository visibility")
async def repo_repository_change(data: RepoRepositoryChange):
    """
    Change repository visibility.

    Maps to: ``devil repo repository change repo_type repo_name repo_visibility``.
    """
    if data.repo_visibility is None:
        raise HTTPException(status_code=400, detail="repo_visibility required")
    args = [
        "--json",
        "repo",
        "repository",
        "change",
        data.repo_type,
        data.repo_name,
        data.repo_visibility,
    ]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/account/add", summary="Add repository account")
async def repo_account_add(data: RepoAccountAdd):
    """
    Add a repository user account (password optional; system may prompt normally).

    Maps to: ``devil repo account add repo_type repo_name repo_username`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = [
        "--json",
        "repo",
        "account",
        "add",
        data.repo_type,
        data.repo_name,
        data.repo_username,
    ]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete(
    "/account/{repo_type}/{repo_name}/{repo_username}",
    summary="Delete repository account",
)
async def repo_account_del(
    repo_type: RepoType = Path(..., description="Repository type: pub or priv"),
    repo_name: str = Path(..., description="Repository name"),
    repo_username: str = Path(..., description="Repository username"),
):
    """
    Delete a repository account.

    Maps to: ``devil repo account del repo_type repo_name repo_username``.
    """
    args = ["--json", "repo", "account", "del", repo_type, repo_name, repo_username]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/account/passwd", summary="Change repository account password")
async def repo_account_passwd(data: RepoAccountPasswd):
    """
    Change repository account password.

    Maps to: ``devil repo account passwd repo_type repo_name repo_username`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = [
        "--json",
        "repo",
        "account",
        "passwd",
        data.repo_type,
        data.repo_name,
        data.repo_username,
    ]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/list", summary="List repositories or accounts")
async def repo_list(
    repo_type: RepoType | None = Query(
        None,
        description="Optional repository type to filter list (requires repo_name if provided)",
    ),
    repo_name: str | None = Query(
        None, description="Optional repository name (requires repo_type when provided)"
    ),
):
    """
    List repositories or accounts for a repository.

    Maps to: ``devil repo list [repo_type repo_name]``.
    Provide both repo_type and repo_name to narrow to accounts.
    """
    args = ["--json", "repo", "list"]
    if repo_type and repo_name:
        args.extend([repo_type, repo_name])
    elif repo_type or repo_name:
        raise HTTPException(
            status_code=400, detail="Provide both repo_type and repo_name or neither"
        )
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
