#!/usr/bin/env python3
"""Check bundled schema provenance against upstream canonical URLs."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.request import urlopen

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, eprint, list_supported_schema_versions, normalize_exit_code, repo_root, schema_path_for_version  # type: ignore
else:
    from ._common import UsageError, eprint, list_supported_schema_versions, normalize_exit_code, repo_root, schema_path_for_version


SCHEMA_URL_TEMPLATE = "https://rqml.org/schema/rqml-{version}.xsd"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_url(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:  # nosec B310 - intended provenance fetch
        return response.read()


def compare_schema(version: str) -> Tuple[bool, str]:
    local_path = schema_path_for_version(version)
    local_bytes = local_path.read_bytes()
    local_hash = sha256_bytes(local_bytes)

    upstream_url = SCHEMA_URL_TEMPLATE.format(version=version)
    upstream_bytes = fetch_url(upstream_url)
    upstream_hash = sha256_bytes(upstream_bytes)

    if local_bytes == upstream_bytes:
        return True, f"{version}: match local={local_hash} upstream={upstream_hash}"
    return False, f"{version}: mismatch local={local_hash} upstream={upstream_hash}"


def run_provenance_check() -> List[Tuple[bool, str]]:
    results: List[Tuple[bool, str]] = []
    for version in list_supported_schema_versions(repo_root()):
        results.append(compare_schema(version))
    return results


def main() -> int:
    results = run_provenance_check()
    failed = False
    for ok, message in results:
        prefix = "OK" if ok else "MISMATCH"
        print(f"{prefix} {message}")
        if not ok:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
    except Exception as exc:
        eprint(str(exc))
        sys.exit(2)
