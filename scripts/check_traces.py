#!/usr/bin/env python3
"""Resolve non-local trace targets in an RQML document."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, build_parser, eprint, ensure_file, normalize_exit_code  # type: ignore
    from scripts._trace import resolve_trace_locators  # type: ignore
else:
    from ._common import UsageError, build_parser, eprint, ensure_file, normalize_exit_code
    from ._trace import resolve_trace_locators


def parse_args() -> object:
    return build_parser("Resolve doc and external trace targets in an RQML document").parse_args()


def main() -> int:
    args = parse_args()
    if not args.target:
        raise UsageError("A target .rqml file is required")

    target = ensure_file(Path(args.target), "target document")
    results = resolve_trace_locators(target)

    if not results:
        print("TRACE OK no doc/external locators found")
        return 0

    failed = False
    for result in results:
        prefix = "OK" if result.ok else "UNRESOLVED"
        print(
            f"{prefix} edge={result.locator.edge_id} direction={result.locator.direction} "
            f"type={result.locator.locator_type} message={result.message}"
        )
        if not result.ok:
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
