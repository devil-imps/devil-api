from __future__ import annotations

import os
from unittest.mock import AsyncMock
from unittest.mock import patch

from fastapi.testclient import TestClient

# Ensure key before import
os.environ.setdefault("DEVIL_API_KEY", "devil")
from app.main import app

client = TestClient(app)


def test_protected_endpoint_requires_api_key():
    r = client.get("/info/limits")
    assert r.status_code == 401
    assert r.json()["detail"].lower().startswith("invalid")


def test_protected_endpoint_with_api_key():
    # Patch execute_devil_command to avoid real socket interaction
    with patch(
        "app.api.endpoints.info.execute_devil_command",
        new=AsyncMock(return_value={"code": "OK", "limits": []}),
    ):
        r = client.get(
            "/info/limits", headers={"X-API-Key": os.environ["DEVIL_API_KEY"]}
        )
    assert r.status_code == 200
    assert r.json()["code"] == "OK"
