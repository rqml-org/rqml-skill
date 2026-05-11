#!/usr/bin/env python3
"""XML parsing helpers for RQML documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET

from _common import UsageError, ensure_file

RQML_NS_21 = "https://rqml.org/schema/2.1.0"
RQML_NS_20 = "https://rqml.org/schema/2.0.1"
RQML_NS_PREFIX = "https://rqml.org/schema/"


@dataclass(frozen=True)
class ParsedXml:
    path: Path
    tree: ET.ElementTree
    root: ET.Element
    namespace: Optional[str]
    version: Optional[str]


def detect_namespace(tag: str) -> Optional[str]:
    if tag.startswith("{") and "}" in tag:
        return tag[1:].split("}", 1)[0]
    return None


def parse_xml(path: Path) -> ParsedXml:
    target = ensure_file(path, "xml document")
    try:
        tree = ET.parse(str(target))
    except ET.ParseError as exc:
        raise UsageError(f"Failed to parse XML: {target}: {exc}") from exc
    root = tree.getroot()
    namespace = detect_namespace(root.tag)
    version = root.attrib.get("version")
    return ParsedXml(path=target, tree=tree, root=root, namespace=namespace, version=version)


def parse_root_metadata(path: Path) -> ParsedXml:
    return parse_xml(path)


def detect_version(path: Path) -> str:
    parsed = parse_root_metadata(path)
    if not parsed.version:
        raise UsageError(f"Missing rqml@version in document: {parsed.path}")
    return parsed.version


def is_rqml_namespace(namespace: Optional[str]) -> bool:
    return bool(namespace and namespace.startswith(RQML_NS_PREFIX))
