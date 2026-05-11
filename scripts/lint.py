#!/usr/bin/env python3
"""Semantic lint for RQML documents with runtime strictness selection."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, build_parser, ensure_file, eprint, normalize_exit_code  # type: ignore
    from scripts._strictness import resolve_strictness  # type: ignore
    from scripts._xml import parse_xml  # type: ignore
else:
    from ._common import UsageError, build_parser, ensure_file, eprint, normalize_exit_code
    from ._strictness import resolve_strictness
    from ._xml import parse_xml


def parse_args() -> object:
    parser = build_parser("Lint an RQML document using strictness-aware semantic rules")
    parser.add_argument(
        "--strictness",
        help="Override detected strictness level (relaxed, standard, strict, certified)",
    )
    return parser.parse_args()


def _local_name(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _iter_elements(root: ET.Element, name: str) -> List[ET.Element]:
    return [element for element in root.iter() if _local_name(element.tag) == name]


def _trace_edges(root: ET.Element) -> List[ET.Element]:
    return _iter_elements(root, "edge")


def _requirements(root: ET.Element) -> List[ET.Element]:
    return _iter_elements(root, "req")


def _criterion_children(req: ET.Element) -> List[ET.Element]:
    for child in req:
        if _local_name(child.tag) == "acceptance":
            return [grandchild for grandchild in child if _local_name(grandchild.tag) == "criterion"]
    return []


def lint_requirements_have_acceptance(root: ET.Element) -> List[str]:
    violations: List[str] = []
    for req in _requirements(root):
        req_id = req.attrib.get("id", "<unknown>")
        criteria = _criterion_children(req)
        if not criteria:
            violations.append(f"{req_id}: missing acceptance criteria")
    return violations


def lint_trace_presence(root: ET.Element) -> List[str]:
    edges = _trace_edges(root)
    if not edges:
        return ["No trace edges found; strict mode requires trace edges on every change"]
    return []


def lint_certified_trace_metadata(root: ET.Element) -> List[str]:
    violations: List[str] = []
    for edge in _trace_edges(root):
        edge_id = edge.attrib.get("id", "<unknown>")
        for attribute in ("createdBy", "createdAt", "confidence"):
            if attribute not in edge.attrib or not edge.attrib.get(attribute):
                violations.append(f"{edge_id}: missing trace metadata attribute {attribute}")
    return violations


def run_lint(target: Path, strictness_override: str | None) -> Tuple[str, str, List[str]]:
    parsed = parse_xml(target)
    resolution = resolve_strictness(strictness_override, target.parent)

    violations: List[str] = []
    if resolution.level in {"standard", "strict", "certified"}:
        violations.extend(lint_requirements_have_acceptance(parsed.root))
    if resolution.level in {"strict", "certified"}:
        violations.extend(lint_trace_presence(parsed.root))
    if resolution.level == "certified":
        violations.extend(lint_certified_trace_metadata(parsed.root))

    return resolution.level, resolution.source, violations


def main() -> int:
    args = parse_args()
    if not args.target:
        raise UsageError("A target .rqml file is required")

    target = ensure_file(Path(args.target), "target document")
    level, source, violations = run_lint(target, args.strictness)

    print(f"STRICTNESS level={level} source={source}")
    if violations:
        for violation in violations:
            eprint(f"LINT {violation}")
        return 1

    print("LINT OK")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
