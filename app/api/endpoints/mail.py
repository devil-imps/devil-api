from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from fastapi import status

from app.schemas.mail import MailAccountAdd
from app.schemas.mail import MailAliasAdd
from app.schemas.mail import MailDKIM
from app.schemas.mail import MailOptions
from app.schemas.mail import MailPasswd
from app.schemas.mail import MailQuota
from app.schemas.mail import MailWhitelist
from app.services.socket_client import DevilSocketError
from app.services.socket_client import execute_devil_command

router = APIRouter(prefix="/mail", tags=["mail"])


@router.post("/account/add", summary="Add mail account")
async def mail_account_add(data: MailAccountAdd):
    """
    Create a mail account.

    Maps to: ``devil mail account add email_mailbox`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "mail", "account", "add", data.email_mailbox]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/account/{email_mailbox}", summary="Delete mail account")
async def mail_account_del(
    email_mailbox: str = Path(..., description="Email mailbox to delete"),
):
    """
    Delete a mail account.

    Maps to: ``devil mail account del email_mailbox``.
    """
    args = ["--json", "mail", "account", "del", email_mailbox]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/alias/add", summary="Add mail alias")
async def mail_alias_add(data: MailAliasAdd):
    """
    Add an email alias.

    Maps to: ``devil mail alias add email_from email_to``.
    """
    args = ["--json", "mail", "alias", "add", data.email_from, data.email_to]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/alias/{email_from}", summary="Delete mail alias")
async def mail_alias_del(
    email_from: str = Path(..., description="Email alias to delete"),
):
    """
    Delete an email alias.

    Maps to: ``devil mail alias del email_from``.
    """
    args = ["--json", "mail", "alias", "del", email_from]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.put("/passwd", summary="Change mail password")
async def mail_passwd(data: MailPasswd):
    """
    Change password for a mail account.

    Maps to: ``devil mail passwd email_mailbox`` (interactive password supplied via API or generated randomly if not provided).
    """
    args = ["--json", "mail", "passwd", data.email_mailbox]
    if data.password:
        args.append(data.password)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


# TODO: Add validation for option values
@router.put("/options", summary="Change mail option")
async def mail_options(data: MailOptions):
    """
    Change a mail domain option.

    Maps to: ``devil mail options email_domain email_option value`` where value matches option contract (on/off, restrictspf modes, IPs etc.).
    """
    args = ["--json", "mail", "options", data.email_domain, data.option, data.value]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.put("/quota", summary="Change mail quota or recalc")
async def mail_quota(data: MailQuota):
    """
    Change or recalc mail quota for an account.

    Maps to: ``devil mail quota email_mailbox mail_quota|recalc``.
    """
    args = ["--json", "mail", "quota", data.email_mailbox, data.mail_quota]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/list", summary="List mail domains or accounts")
async def mail_list(
    email_domain: str | None = Query(
        None, description="Optional email domain to filter results"
    ),
):
    """
    List mail domains OR mailbox+aliases for a domain.

    Maps to: ``devil mail list [email_domain]``.
    """
    args = ["--json", "mail", "list"]
    if email_domain:
        args.append(email_domain)
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/whitelist/add", summary="Add mail whitelist domain")
async def mail_whitelist_add(data: MailWhitelist):
    """
    Add a domain to mail whitelist.

    Maps to: ``devil mail whitelist add domain``.
    """
    args = ["--json", "mail", "whitelist", "add", data.domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/whitelist/{domain}", summary="Delete mail whitelist domain")
async def mail_whitelist_del(
    domain: str = Path(..., description="Domain to remove from whitelist"),
):
    """
    Remove a domain from mail whitelist.

    Maps to: ``devil mail whitelist del domain``.
    """
    args = ["--json", "mail", "whitelist", "del", domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/whitelist/list", summary="List mail whitelist domains")
async def mail_whitelist_list():
    """
    List all whitelisted mail domains.

    Maps to: ``devil mail whitelist list``.
    """
    args = ["--json", "mail", "whitelist", "list"]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/dkim/sign", summary="Sign domain with DKIM")
async def mail_dkim_sign(data: MailDKIM):
    """
    Create DKIM key and sign a domain.

    Maps to: ``devil mail dkim sign domain``.
    """
    args = ["--json", "mail", "dkim", "sign", data.domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/dkim/dns/{domain}", summary="Get DKIM DNS record")
async def mail_dkim_dns(
    domain: str = Path(..., description="Domain to get DKIM DNS record for"),
    print_record: bool = Query(
        False, description="Whether to print the DKIM DNS record"
    ),
):
    """
    Add or print DKIM DNS record.

    Maps to: ``devil mail dkim dns domain [--print]``.
    Set print_record=true to append --print.
    """
    args = ["--json", "mail", "dkim", "dns", domain]
    if print_record:
        args.append("--print")
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.delete("/dkim/unsign/{domain}", summary="Remove DKIM key")
async def mail_dkim_unsign(
    domain: str = Path(..., description="Domain to remove DKIM key for"),
):
    """
    Remove DKIM key for a domain.

    Maps to: ``devil mail dkim unsign domain``.
    """
    args = ["--json", "mail", "dkim", "unsign", domain]
    try:
        return await execute_devil_command(args)
    except DevilSocketError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
