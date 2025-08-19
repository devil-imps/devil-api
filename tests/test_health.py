from __future__ import annotations

import os

from fastapi.testclient import TestClient

# Ensure API key exists before importing app (app validates at import time)
os.environ.setdefault("DEVIL_API_KEY", "devil")

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
