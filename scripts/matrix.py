#!/usr/bin/env python3
"""Generate a Markdown traceability matrix from an RQML document."""

from __future__ import annotations

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


TRACE_TYPES = ["satisfies", "dependsOn", "mitigates", "verifiedBy"]


def parse_args() -> object:
    return build_parser("Generate a Markdown traceability matrix from an RQML document").parse_args()


def _local_name(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _first_child(element: ET.Element, name: str) -> ET.Element | None:
    for child in element:
        if _local_name(child.tag) == name:
            return child
    return None


def extract_requirements_and_traces(path: Path) -> List[Dict[str, object]]:
    parsed = parse_xml(path)
    requirements: List[Dict[str, object]] = []
    requirement_ids: Dict[str, Dict[str, object]] = {}

    for element in parsed.root.iter():
        if _local_name(element.tag) != "req":
            continue
        req_id = element.attrib.get("id")
        if not req_id:
            continue
        record = {
            "id": req_id,
            "title": element.attrib.get("title", ""),
            "satisfies": [],
            "dependsOn": [],
            "mitigates": [],
            "verifiedBy": [],
        }
        requirements.append(record)
        requirement_ids[req_id] = record

    for edge in parsed.root.iter():
        if _local_name(edge.tag) != "edge":
            continue
        edge_type = edge.attrib.get("type")
        if edge_type not in TRACE_TYPES:
            continue

        from_element = _first_child(edge, "from")
        to_element = _first_child(edge, "to")
        if from_element is None or to_element is None:
            continue

        from_locator = _first_child(from_element, "locator")
        to_locator = _first_child(to_element, "locator")
        if from_locator is None or to_locator is None:
            continue

        from_ref = None
        to_ref = None
        for child in from_locator:
            if _local_name(child.tag) == "local":
                from_ref = child.attrib.get("id")
                break
        for child in to_locator:
            if _local_name(child.tag) == "local":
                to_ref = child.attrib.get("id")
                break

        if from_ref in requirement_ids and to_ref:
            requirement_ids[from_ref][edge_type].append(to_ref)

    requirements.sort(key=lambda item: item["id"])
    return requirements


def render_matrix(rows: List[Dict[str, object]]) -> str:
    header = "| Requirement | Title | Satisfies | Depends On | Mitigates | Verified By |"
    divider = "|---|---|---|---|---|---|"
    lines = [header, divider]

    for row in rows:
        lines.append(
            "| {id} | {title} | {satisfies} | {dependsOn} | {mitigates} | {verifiedBy} |".format(
                id=row["id"],
                title=row["title"],
                satisfies=", ".join(row["satisfies"]),
                dependsOn=", ".join(row["dependsOn"]),
                mitigates=", ".join(row["mitigates"]),
                verifiedBy=", ".join(row["verifiedBy"]),
            )
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if not args.target:
        raise UsageError("A target .rqml file is required")

    target = ensure_file(Path(args.target), "target document")
    rows = extract_requirements_and_traces(target)
    print(render_matrix(rows))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
