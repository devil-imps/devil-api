from __future__ import annotations

from enum import Enum

__all__ = ["VHostType"]


class VHostType(str, Enum):
    private = "private"
    public = "public"
    all = "all"
