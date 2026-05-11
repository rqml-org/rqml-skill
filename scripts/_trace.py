#!/usr/bin/env python3
"""Trace parsing and resolution helpers for RQML documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

if __package__ in (None, ""):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._common import UsageError, ensure_file, repo_root  # type: ignore
    from scripts._xml import parse_xml  # type: ignore
else:
    from ._common import UsageError, ensure_file, repo_root
    from ._xml import parse_xml


@dataclass(frozen=True)
class TraceLocator:
    edge_id: str
    direction: str
    locator_type: str
    uri: Optional[str]
    doc_id: Optional[str]
    local_id: Optional[str]
    title: Optional[str]


@dataclass(frozen=True)
class TraceResolution:
    locator: TraceLocator
    ok: bool
    message: str


def _local_name(tag: str) -> str:
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _first_child(element: ET.Element, name: str) -> Optional[ET.Element]:
    for child in element:
        if _local_name(child.tag) == name:
            return child
    return None


def load_trace_locators(path: Path) -> List[TraceLocator]:
    parsed = parse_xml(path)
    locators: List[TraceLocator] = []

    for edge in parsed.root.iter():
        if _local_name(edge.tag) != "edge":
            continue
        edge_id = edge.attrib.get("id", "<unknown>")
        for direction in ("from", "to"):
            endpoint = _first_child(edge, direction)
            if endpoint is None:
                continue
            locator_wrapper = _first_child(endpoint, "locator")
            if locator_wrapper is None:
                continue
            for locator_child in locator_wrapper:
                locator_type = _local_name(locator_child.tag)
                locators.append(
                    TraceLocator(
                        edge_id=edge_id,
                        direction=direction,
                        locator_type=locator_type,
                        uri=locator_child.attrib.get("uri"),
                        doc_id=locator_child.attrib.get("docId"),
                        local_id=locator_child.attrib.get("id"),
                        title=locator_child.attrib.get("title"),
                    )
                )
                break
    return locators


def resolve_doc_locator(locator: TraceLocator, base: Path) -> TraceResolution:
    if not locator.uri:
        return TraceResolution(locator=locator, ok=False, message="doc locator missing uri")

    if locator.uri.startswith("file:"):
        candidate = Path(locator.uri[5:])
    else:
        candidate = Path(locator.uri)
        if not candidate.is_absolute():
            candidate = (base / candidate).resolve()

    if not candidate.exists() or not candidate.is_file():
        return TraceResolution(locator=locator, ok=False, message=f"unresolved doc target: {candidate}")

    try:
        parsed = parse_xml(candidate)
    except UsageError as exc:
        return TraceResolution(locator=locator, ok=False, message=str(exc))

    if locator.local_id:
        found = False
        for element in parsed.root.iter():
            if element.attrib.get("id") == locator.local_id:
                found = True
                break
        if not found:
            return TraceResolution(
                locator=locator,
                ok=False,
                message=f"doc target found but id {locator.local_id!r} was not present",
            )

    return TraceResolution(locator=locator, ok=True, message=f"resolved doc target: {candidate}")


def resolve_external_locator(locator: TraceLocator) -> TraceResolution:
    if not locator.uri:
        return TraceResolution(locator=locator, ok=False, message="external locator missing uri")

    parsed_uri = urlparse(locator.uri)
    if parsed_uri.scheme in {"http", "https"}:
        return TraceResolution(locator=locator, ok=True, message=f"external HTTP target parsed: {locator.uri}")
    if parsed_uri.scheme == "file":
        candidate = Path(parsed_uri.path)
        if candidate.exists():
            return TraceResolution(locator=locator, ok=True, message=f"external file target exists: {candidate}")
        return TraceResolution(locator=locator, ok=False, message=f"external file target missing: {candidate}")
    if parsed_uri.scheme:
        return TraceResolution(locator=locator, ok=True, message=f"external URI scheme accepted: {parsed_uri.scheme}")
    return TraceResolution(locator=locator, ok=False, message=f"external locator is not a valid URI: {locator.uri}")


def resolve_trace_locators(path: Path) -> List[TraceResolution]:
    target = ensure_file(path, "target document")
    base = target.parent
    results: List[TraceResolution] = []

    for locator in load_trace_locators(target):
        if locator.locator_type == "doc":
            results.append(resolve_doc_locator(locator, base))
        elif locator.locator_type == "external":
            results.append(resolve_external_locator(locator))
    return results
