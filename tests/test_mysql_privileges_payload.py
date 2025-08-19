from __future__ import annotations

import os
from unittest.mock import AsyncMock
from unittest.mock import patch

from fastapi.testclient import TestClient

os.environ.setdefault("DEVIL_API_KEY", "devil")
from app.main import app

client = TestClient(app)


def test_mysql_privileges_all_only():
    with patch(
        "app.api.endpoints.mysql.execute_devil_command",
        new=AsyncMock(return_value={"code": "OK", "args": []}),
    ):
        r = client.put(
            "/mysql/privileges",
            headers={"X-API-Key": os.environ["DEVIL_API_KEY"]},
            json={
                "user_name": "test",
                "host_name": "test123",
                "database_name": "test321",
                "mysql_privileges": ["+ALL"],
            },
        )
    assert r.status_code == 200, r.text


def test_mysql_privileges_conflict_rejected():
    # +ALL with another should 422 (validation error)
    with patch(
        "app.api.endpoints.mysql.execute_devil_command",
        new=AsyncMock(return_value={"code": "OK"}),
    ):
        r = client.put(
            "/mysql/privileges",
            headers={"X-API-Key": os.environ["DEVIL_API_KEY"]},
            json={
                "user_name": "u",
                "database_name": "d",
                "mysql_privileges": ["+ALL", "+SELECT"],
            },
        )
    assert r.status_code == 422
    detail = r.json()["detail"]
    assert any("ALL" in (err.get("msg", "") or "") for err in detail), detail
