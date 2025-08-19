from __future__ import annotations

import os
from unittest.mock import AsyncMock
from unittest.mock import patch

from fastapi.testclient import TestClient

os.environ.setdefault("DEVIL_API_KEY", "devil")
from app.auth import AUTH_FAIL_THRESHOLD
from app.main import app

client = TestClient(app)


def test_bearer_token_alias():
    # Patch to avoid real socket call
    with patch(
        "app.api.endpoints.info.execute_devil_command",
        new=AsyncMock(return_value={"code": "OK"}),
    ):
        r = client.get(
            "/info/limits",
            headers={"Authorization": f"Bearer {os.environ['DEVIL_API_KEY']}"},
        )
    assert r.status_code == 200
    assert r.json()["code"] == "OK"


def test_rate_limiting_on_failures():
    # Intentionally send wrong key until block triggers
    wrong_headers = {"X-API-Key": "wrong"}
    # perform threshold attempts
    for i in range(AUTH_FAIL_THRESHOLD):
        r = client.get("/info/limits", headers=wrong_headers)
        # Expect 401 until possibly last becomes 429
        if i < AUTH_FAIL_THRESHOLD - 1:
            assert r.status_code == 401
        else:
            # Last attempt should produce 429 or still 401 if logic changes threshold interpretation
            assert r.status_code in (401, 429)
    # Next attempt should be 429
    r2 = client.get("/info/limits", headers=wrong_headers)
    assert r2.status_code == 429
