from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

# Adjust sys.path early so subsequent imports resolve
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Provide default API key before importing modules that validate it at import time
os.environ.setdefault("DEVIL_API_KEY", "devil")

# Lazy import after env var is ensured while keeping all import statements grouped at the top
AUTH_FAILURE_TRACKER = importlib.import_module("app.auth").AUTH_FAILURE_TRACKER


@pytest.fixture(autouse=True)
def reset_auth_tracker():
    """Reset authentication failure tracker between tests to avoid bleed-over."""
    AUTH_FAILURE_TRACKER.clear()
    yield
    AUTH_FAILURE_TRACKER.clear()
