from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field

__all__ = [
    "WWWAdd",
    "WWWDel",
    "WWWEnvironment",
    "WWWOptions",
    "WWWOptionsEnum",
    "WWWStatsAccessAdd",
    "WWWStatsAccessDel",
    "WWWStatsAccountAdd",
    "WWWStatsAccountDel",
    "WWWStatsAccountPasswd",
    "WWWStatsDomainAdd",
    "WWWStatsDomainDel",
    "WWWType",
]


class WWWType(str, Enum):
    php = "php"
    python = "python"
    ruby = "ruby"
    nodejs = "nodejs"
    proxy = "proxy"
    pointer = "pointer"


class WWWEnvironment(str, Enum):
    production = "production"
    staging = "staging"
    development = "development"
    test = "test"


class WWWOptionsEnum(str, Enum):
    GZIP = "gzip"
    SSL_ONLY = "sslonly"
    PLNET = "plnet"
    PHP_EVAL = "php_eval"
    PHP_EXEC = "php_exec"
    PHP_OPEN_BASE_DIR = "php_openbasedir"
    CACHE = "cache"
    CACHE_COOKIE = "cache_cookie"
    CACHE_DEBUG = "cache_debug"
    WAF = "waf"
    BLACKLIST = "blacklist"
    STATS_ANONYMIZE = "stats_anonymize"
    STATS_EXCLUDE = "stats_exclude"
    PROCESSES = "processes"
    TLS_MIN = "tls_min"


class WWWAdd(BaseModel):
    www_domain: str = Field(..., description="Domain name")
    www_type: WWWType | None = Field(
        None, description="php, python, ruby, nodejs, proxy, pointer"
    )
    pointer_target: str | None = Field(None, description="Pointer target domain")
    proxy_target: str | None = Field(None, description="Proxy target host")
    proxy_port: int | None = Field(None, description="Proxy port")
    passenger_binary: str | None = Field(
        None, description="Passenger binary path for python/nodejs/ruby"
    )
    www_environment: WWWEnvironment | None = Field(
        None, description="Passenger environment"
    )


class WWWDel(BaseModel):
    www_domain: str = Field(..., description="Domain to delete")
    remove: bool = Field(False, description="Also remove domain data using --remove")


class WWWOptions(BaseModel):
    www_domain: str = Field(..., description="Domain name")
    www_option: WWWOptionsEnum = Field(
        ...,
        description="Website option, choose from: gzip (on|off), sslonly (on|off), plnet (on|off), php_eval (on|off), php_exec (on|off), php_openbasedir (dirs), cache (control|short|long|purge|off), cache_cookie (any|none|name), cache_debug (on|off), waf (0|1|2|3|4|5), blacklist (0|1|2|3|4), stats_anonymize (on|off), stats_exclude (comma-separated IP addresses), processes (1+), tls_min (1.0|1.1|1.2|1.3)",
    )
    value: str = Field(..., description="Option value according to selected key")


class WWWStatsAccountAdd(BaseModel):
    user_name: str = Field(..., description="Matomo stats username to create")
    password: str | None = Field(
        None, description="Optional password, generated randomly if not provided"
    )


class WWWStatsAccountDel(BaseModel):
    user_name: str = Field(..., description="Matomo stats username to delete")


class WWWStatsAccountPasswd(BaseModel):
    user_name: str = Field(
        ..., description="Matomo stats username to change password for"
    )
    password: str | None = Field(
        None, description="New password, generated randomly if not provided"
    )


class WWWStatsAccessAdd(BaseModel):
    www_domain: str = Field(
        ..., description="Domain name for which to grant stats access"
    )
    user_name: str = Field(..., description="Stats username to grant access to")


class WWWStatsAccessDel(BaseModel):
    www_domain: str = Field(
        ..., description="Domain name whose stats access is revoked"
    )
    user_name: str = Field(..., description="Stats username to revoke access from")


class WWWStatsDomainAdd(BaseModel):
    www_domain: str = Field(..., description="Domain to add to stats tracking")


class WWWStatsDomainDel(BaseModel):
    www_domain: str = Field(..., description="Domain to remove from stats tracking")
