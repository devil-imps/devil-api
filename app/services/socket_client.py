"""
Asynchronous client for communicating with the devil UNIX domain socket.

The devil command accepts a JSON encoded list of string arguments and returns
JSON (object) as response.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Iterable
from typing import Any

SOCKET_PATH = "/var/run/devil2.sock"
SOCKET_TIMEOUT = 30  # seconds


class DevilSocketError(RuntimeError):
    """Base exception for devil socket errors."""


class DevilSocketConnectionError(DevilSocketError):
    """Raised when connection to socket fails."""


class DevilSocketProtocolError(DevilSocketError):
    """Raised when response cannot be parsed or is not JSON object."""


logger = logging.getLogger(__name__)


async def execute_devil_command(args: Iterable[str]) -> dict[str, Any]:
    """
    Execute devil command via UNIX domain socket and return parsed JSON.

    Args:
        args: Iterable of arguments; '--json' must be first (caller ensures).

    Returns:
        Parsed JSON object (dict).

    Raises:
        DevilSocketConnectionError: on connection issues.
        DevilSocketProtocolError: on invalid JSON or non-object response.
        DevilSocketError: on reported error response with code != OK.
    """
    arg_list = list(args)
    data = json.dumps(arg_list)

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_unix_connection(SOCKET_PATH), timeout=SOCKET_TIMEOUT
        )
    except (OSError, TimeoutError) as exc:  # pragma: no cover - environment specific
        raise DevilSocketConnectionError(
            f"Cannot connect to devil socket: {exc}"
        ) from exc

    try:
        writer.write(data.encode() + b"\n")  # newline termination for nc style
        await writer.drain()

        # Read until EOF (socket closes) or newline; implement timeout.
        try:
            raw = await asyncio.wait_for(reader.read(), timeout=SOCKET_TIMEOUT)
        except TimeoutError as exc:
            raise DevilSocketConnectionError(
                "Timeout waiting for devil response"
            ) from exc

        if not raw:
            raise DevilSocketProtocolError("Empty response from devil socket")

        text = raw.decode().strip()
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as exc:
            raise DevilSocketProtocolError(
                f"Invalid JSON from devil socket: {text[:200]}"
            ) from exc

        if not isinstance(obj, dict):
            raise DevilSocketProtocolError(
                "Devil response must be a JSON object (dict)"
            )

        # devil error convention
        if obj.get("code") == "ERROR":
            # propagate as 400-level error - raise and let route handler map
            raise DevilSocketError(obj.get("msg", "devil/error"))
        return obj
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception as exc:  # pragma: no cover - best effort cleanup
            logger.debug("Error closing devil socket writer: %s", exc)
