#!/usr/bin/env python3
"""Normalized reporting helpers for validation and lint scripts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional
import json


@dataclass
class ValidationErrorItem:
    line: int
    column: Optional[int]
    path: Optional[str]
    message: str
    severity: str
    suggestion: Optional[str] = None


@dataclass
class Report:
    ok: bool
    backend: Optional[str]
    schema: Optional[str]
    errors: List[ValidationErrorItem]

    def to_dict(self) -> Dict[str, object]:
        return {
            "ok": self.ok,
            "backend": self.backend,
            "schema": self.schema,
            "errors": [asdict(error) for error in self.errors],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


def success_report(backend: Optional[str], schema: Optional[str]) -> Report:
    return Report(ok=True, backend=backend, schema=schema, errors=[])


def failure_report(
    backend: Optional[str], schema: Optional[str], errors: List[ValidationErrorItem]
) -> Report:
    return Report(ok=False, backend=backend, schema=schema, errors=errors)
