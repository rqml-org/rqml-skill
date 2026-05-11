#!/usr/bin/env python3
"""Common cross-platform helpers for RQML skill scripts."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


REPO_MARKERS = ("requirements.rqml", ".rqml")
SUPPORTED_SCHEMA_GLOB = "rqml-*.xsd"


class RqmlError(Exception):
    """Base error for script-friendly failures."""


class UsageError(RqmlError):
    """Raised for invalid user input or unsupported invocation."""


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def repo_root(start: Optional[Path] = None) -> Path:
    current = (start or script_dir()).resolve()
    for candidate in [current, *current.parents]:
        if all((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    if (script_dir().parent / "requirements.rqml").exists():
        return script_dir().parent
    raise UsageError("Could not determine repository root from current workspace")


def ensure_file(path: Path, label: str = "file") -> Path:
    candidate = path.expanduser().resolve()
    if not candidate.exists() or not candidate.is_file():
        raise UsageError(f"{label.capitalize()} not found: {candidate}")
    return candidate


def ensure_dir(path: Path, label: str = "directory") -> Path:
    candidate = path.expanduser().resolve()
    if not candidate.exists() or not candidate.is_dir():
        raise UsageError(f"{label.capitalize()} not found: {candidate}")
    return candidate


def bundled_schema_dir(root: Optional[Path] = None) -> Path:
    return ensure_dir(repo_root(root) / "references" / "schemas", "schema directory")


def list_supported_schema_versions(root: Optional[Path] = None) -> List[str]:
    schema_root = bundled_schema_dir(root)
    versions = []
    for schema_path in sorted(schema_root.glob(SUPPORTED_SCHEMA_GLOB)):
        stem = schema_path.stem
        prefix = "rqml-"
        if stem.startswith(prefix):
            versions.append(stem[len(prefix):])
    return versions


def schema_path_for_version(version: str, root: Optional[Path] = None) -> Path:
    path = bundled_schema_dir(root) / f"rqml-{version}.xsd"
    if not path.exists():
        supported = ", ".join(list_supported_schema_versions(root)) or "none"
        raise UsageError(
            f"No bundled schema for version {version!r}. Supported versions: {supported}"
        )
    return path.resolve()


def which(command: str) -> Optional[str]:
    return shutil.which(command)


def run_command(
    command: Sequence[str],
    cwd: Optional[Path] = None,
    env: Optional[dict] = None,
    timeout: Optional[float] = None,
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            list(command),
            cwd=str(cwd) if cwd else None,
            env=env,
            timeout=timeout,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise UsageError(f"Command not found: {command[0]}") from exc


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "target",
        nargs="?",
        help="Path to the target .rqml document",
    )
    return parser


def normalize_exit_code(value: int) -> int:
    if value < 0:
        return 1
    if value > 255:
        return 255
    return value


def eprint(*parts: object) -> None:
    print(*parts, file=sys.stderr)


def is_windows() -> bool:
    return os.name == "nt"


def as_posix_path(path: Path) -> str:
    return path.resolve().as_posix()


def coalesce(*values: Optional[str]) -> Optional[str]:
    for value in values:
        if value:
            return value
    return None


def join_nonempty(values: Iterable[str], separator: str = ", ") -> str:
    return separator.join([value for value in values if value])
