#!/usr/bin/env python3
"""Strictness discovery helpers for RQML semantic linting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Optional

if __package__ in (None, ""):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, repo_root  # type: ignore
else:
    from ._common import UsageError, repo_root


STRICTNESS_VALUES = {"relaxed", "standard", "strict", "certified"}
AGENTS_PATTERN = re.compile(r"^##\s+Strictness:\s+`(?P<level>relaxed|standard|strict|certified)`\s*$", re.MULTILINE)
YAML_PATTERN = re.compile(r"^strictness:\s*(?P<level>relaxed|standard|strict|certified)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class StrictnessResolution:
    level: str
    source: str


def _validate_level(level: str) -> str:
    normalized = level.strip().lower()
    if normalized not in STRICTNESS_VALUES:
        raise UsageError(
            f"Unsupported strictness {level!r}. Expected one of: {', '.join(sorted(STRICTNESS_VALUES))}"
        )
    return normalized


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_from_yaml(path: Path) -> Optional[StrictnessResolution]:
    if not path.exists() or not path.is_file():
        return None
    match = YAML_PATTERN.search(_read_text(path))
    if not match:
        return None
    return StrictnessResolution(level=_validate_level(match.group("level")), source=str(path.name))


def read_from_agents(path: Path) -> Optional[StrictnessResolution]:
    if not path.exists() or not path.is_file():
        return None
    match = AGENTS_PATTERN.search(_read_text(path))
    if not match:
        return None
    return StrictnessResolution(level=_validate_level(match.group("level")), source=str(path.name))


def resolve_strictness(override: Optional[str] = None, start: Optional[Path] = None) -> StrictnessResolution:
    if override:
        return StrictnessResolution(level=_validate_level(override), source="--strictness")

    root = repo_root(start)

    yaml_resolution = read_from_yaml(root / ".rqml-skill.yaml")
    if yaml_resolution:
        return yaml_resolution

    agents_resolution = read_from_agents(root / "AGENTS.md")
    if agents_resolution:
        return agents_resolution

    return StrictnessResolution(level="standard", source="default")
