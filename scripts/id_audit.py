#!/usr/bin/env python3
"""Audit RQML identifiers for duplicates, naming hygiene, and revision drift."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import xml.etree.ElementTree as ET

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, build_parser, eprint, ensure_file, normalize_exit_code  # type: ignore
    from scripts._git import previous_file_content  # type: ignore
    from scripts._xml import parse_xml  # type: ignore
else:
    from ._common import UsageError, build_parser, eprint, ensure_file, normalize_exit_code
    from ._git import previous_file_content
    from ._xml import parse_xml


ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*$")


def parse_args() -> object:
    return build_parser("Audit RQML identifiers for duplicates and naming issues").parse_args()


def extract_ids_from_root(root: ET.Element) -> List[str]:
    ids: List[str] = []
    for element in root.iter():
        identifier = element.attrib.get("id")
        if identifier:
            ids.append(identifier)
    return ids


def extract_ids(path: Path) -> List[str]:
    return extract_ids_from_root(parse_xml(path).root)


def duplicate_ids(ids: List[str]) -> List[str]:
    counts = Counter(ids)
    return sorted([identifier for identifier, count in counts.items() if count > 1])


def malformed_ids(ids: List[str]) -> List[str]:
    return sorted([identifier for identifier in ids if not ID_PATTERN.match(identifier)])


def compare_with_previous(path: Path) -> Optional[Tuple[Set[str], Set[str]]]:
    previous = previous_file_content(path)
    if previous is None:
        return None
    try:
        previous_root = ET.fromstring(previous)
    except ET.ParseError:
        return None

    current_ids = set(extract_ids(path))
    previous_ids = set(extract_ids_from_root(previous_root))
    removed = previous_ids - current_ids
    added = current_ids - previous_ids
    return removed, added


def run_audit(path: Path) -> Dict[str, object]:
    target = ensure_file(path, "target document")
    ids = extract_ids(target)
    duplicates = duplicate_ids(ids)
    malformed = malformed_ids(ids)
    previous = compare_with_previous(target)

    return {
        "duplicates": duplicates,
        "malformed": malformed,
        "previous": previous,
    }


def main() -> int:
    args = parse_args()
    if not args.target:
        raise UsageError("A target .rqml file is required")

    result = run_audit(Path(args.target))
    exit_code = 0

    if result["duplicates"]:
        exit_code = 1
        for identifier in result["duplicates"]:
            eprint(f"DUPLICATE {identifier}")

    if result["malformed"]:
        exit_code = 1
        for identifier in result["malformed"]:
            eprint(f"MALFORMED {identifier}")

    previous = result["previous"]
    if previous is None:
        print("PREVIOUS unavailable")
    else:
        removed, added = previous
        if removed or added:
            exit_code = 1
        for identifier in sorted(removed):
            eprint(f"REMOVED {identifier}")
        for identifier in sorted(added):
            print(f"ADDED {identifier}")

    if exit_code == 0:
        print("ID AUDIT OK")
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
