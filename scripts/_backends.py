#!/usr/bin/env python3
"""Validation backend discovery and metadata."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec
from typing import List, Optional

from _common import which


@dataclass(frozen=True)
class BackendInfo:
    name: str
    available: bool
    reason: Optional[str] = None


def detect_xmllint() -> BackendInfo:
    executable = which("xmllint")
    if executable:
        return BackendInfo(name="xmllint", available=True)
    return BackendInfo(name="xmllint", available=False, reason="xmllint not found on PATH")


def detect_lxml() -> BackendInfo:
    if find_spec("lxml") is not None:
        return BackendInfo(name="lxml", available=True)
    return BackendInfo(name="lxml", available=False, reason="lxml import unavailable")


def detect_xmlschema() -> BackendInfo:
    if find_spec("xmlschema") is not None:
        return BackendInfo(name="xmlschema", available=True)
    return BackendInfo(name="xmlschema", available=False, reason="xmlschema import unavailable")


def available_backends() -> List[BackendInfo]:
    return [detect_xmllint(), detect_lxml(), detect_xmlschema()]


def choose_backend() -> Optional[BackendInfo]:
    for backend in available_backends():
        if backend.available:
            return backend
    return None
