from __future__ import annotations

import logging
import os
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.endpoints import dns
from app.api.endpoints import ftp
from app.api.endpoints import info
from app.api.endpoints import mail
from app.api.endpoints import mongo
from app.api.endpoints import mysql
from app.api.endpoints import pgsql
from app.api.endpoints import port
from app.api.endpoints import repo
from app.api.endpoints import ssl
from app.api.endpoints import vhost
from app.api.endpoints import www
from app.auth import verify_api_key
from app.services.socket_client import DevilSocketConnectionError
from app.services.socket_client import DevilSocketError
from app.services.socket_client import DevilSocketProtocolError

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

# Get package version
try:
    __version__ = version("devil-api")
except PackageNotFoundError:
    __version__ = "0.0.1"

app = FastAPI(title="devil API", version=__version__)


# Include routers
protected_dependency = [Depends(verify_api_key)]

app.include_router(info.router, dependencies=protected_dependency)
app.include_router(ftp.router, dependencies=protected_dependency)
app.include_router(dns.router, dependencies=protected_dependency)
app.include_router(mail.router, dependencies=protected_dependency)
app.include_router(mysql.router, dependencies=protected_dependency)
app.include_router(pgsql.router, dependencies=protected_dependency)
app.include_router(mongo.router, dependencies=protected_dependency)
app.include_router(port.router, dependencies=protected_dependency)
app.include_router(repo.router, dependencies=protected_dependency)
app.include_router(ssl.router, dependencies=protected_dependency)
app.include_router(vhost.router, dependencies=protected_dependency)
app.include_router(www.router, dependencies=protected_dependency)


# Health check endpoint
@app.get("/health", tags=["meta"], include_in_schema=False)
async def health():
    return {"status": "ok"}


# Global exception handlers
@app.exception_handler(DevilSocketConnectionError)
async def handle_connection_error(_: Request, exc: DevilSocketConnectionError):
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.exception_handler(DevilSocketProtocolError)
async def handle_protocol_error(_: Request, exc: DevilSocketProtocolError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(DevilSocketError)
async def handle_command_error(_: Request, exc: DevilSocketError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
