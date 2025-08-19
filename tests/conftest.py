from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from app.auth import AUTH_FAILURE_TRACKER

# Ensure project root (where 'app' package resides) is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Provide default API key for any imports needing it
os.environ.setdefault("DEVIL_API_KEY", "devil")


@pytest.fixture(autouse=True)
def reset_auth_tracker():
    """Reset authentication failure tracker between tests to avoid bleed-over."""
    AUTH_FAILURE_TRACKER.clear()
    yield
    AUTH_FAILURE_TRACKER.clear()
