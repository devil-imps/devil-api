from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field

__all__ = [
    "MailAccountAdd",
    "MailAliasAdd",
    "MailDKIM",
    "MailOptions",
    "MailPasswd",
    "MailQuota",
    "MailWhitelist",
]


class MailOptionsEnum(str, Enum):
    RBL = "rbl"
    SPAMFILTER = "spamfilter"
    RESTRICT_SPF = "restrictspf"
    MOVESPAM = "movespam"
    OUTGOING_IP = "outgoingip"
    ALLOW_NETS = "allownets"
    HIDE_SENDER_IP = "hidesenderip"


class MailAccountAdd(BaseModel):
    email_mailbox: str = Field(..., description="E-mail address for the mailbox")
    password: str | None = Field(
        None,
        description="Plaintext password to set for the mailbox, generated randomly if not provided",
    )


class MailAliasAdd(BaseModel):
    email_from: str = Field(..., description="Source alias address")
    email_to: str = Field(..., description="Target e-mail address")


class MailPasswd(BaseModel):
    email_mailbox: str = Field(..., description="E-mail address to change password for")
    password: str | None = Field(
        None, description="New plaintext password, generated randomly if not provided"
    )


class MailOptions(BaseModel):
    email_domain: str = Field(..., description="Domain name")
    option: MailOptionsEnum = Field(
        ...,
        description="Mail option, choose from: rbl (on|off), spamfilter (on|off), restrictspf (on|off|reject), movespam (on|off), outgoingip (private IP address)|default), allownets (comma-separated IP addresses), hidesenderip (on|off)",
    )
    value: str = Field(..., description="Option value")


class MailQuota(BaseModel):
    email_mailbox: str = Field(..., description="E-mail address")
    mail_quota: str = Field(..., description="Quota value e.g. 2G, 500M or recalc")


class MailWhitelist(BaseModel):
    domain: str = Field(..., description="Domain to whitelist")


class MailDKIM(BaseModel):
    domain: str = Field(..., description="Domain for DKIM operation")
