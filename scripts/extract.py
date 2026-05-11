#!/usr/bin/env python3
"""Extract requirement objects from an RQML document as JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List
import xml.etree.ElementTree as ET

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, build_parser, ensure_file, eprint, normalize_exit_code  # type: ignore
    from scripts._xml import parse_xml  # type: ignore
else:
    from ._common import UsageError, build_parser, ensure_file, eprint, normalize_exit_code
    from ._xml import parse_xml


def parse_args() -> object:
    return build_parser("Extract requirements from an RQML document as JSON").parse_args()


def _local_name(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _text_content(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


def extract_requirements(path: Path) -> List[Dict[str, object]]:
    parsed = parse_xml(path)
    extracted: List[Dict[str, object]] = []

    for element in parsed.root.iter():
        if _local_name(element.tag) != "req":
            continue

        statement = ""
        for child in element:
            if _local_name(child.tag) == "statement":
                statement = _text_content(child)
                break

        extracted.append(
            {
                "id": element.attrib.get("id"),
                "type": element.attrib.get("type"),
                "title": element.attrib.get("title"),
                "priority": element.attrib.get("priority"),
                "status": element.attrib.get("status"),
                "statement": statement,
            }
        )

    extracted.sort(key=lambda item: (item.get("id") or ""))
    return extracted


def main() -> int:
    args = parse_args()
    if not args.target:
        raise UsageError("A target .rqml file is required")

    target = ensure_file(Path(args.target), "target document")
    extracted = extract_requirements(target)
    print(json.dumps(extracted, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
