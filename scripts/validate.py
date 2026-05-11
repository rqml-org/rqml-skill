#!/usr/bin/env python3
"""Validate an RQML document against a bundled XSD schema."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts._backends import BackendInfo, available_backends, choose_backend  # type: ignore
    from scripts._common import (  # type: ignore
        UsageError,
        as_posix_path,
        build_parser,
        eprint,
        ensure_file,
        normalize_exit_code,
        run_command,
        schema_path_for_version,
    )
    from scripts._report import (  # type: ignore
        ValidationErrorItem,
        failure_report,
        success_report,
    )
    from scripts._xml import detect_version  # type: ignore
else:
    from ._backends import BackendInfo, available_backends, choose_backend
    from ._common import (
        UsageError,
        as_posix_path,
        build_parser,
        eprint,
        ensure_file,
        normalize_exit_code,
        run_command,
        schema_path_for_version,
    )
    from ._report import ValidationErrorItem, failure_report, success_report
    from ._xml import detect_version


ERROR_PATTERN = re.compile(r":(?P<line>\d+):(?P<column>\d+):\s*(?P<message>.+)")


def parse_args() -> object:
    parser = build_parser("Validate an RQML document against a bundled schema")
    parser.add_argument(
        "--schema-version",
        help="Override rqml@version and use a specific bundled schema version",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit structured JSON output",
    )
    return parser.parse_args()


def detect_schema(target: Path, override_version: Optional[str]) -> Path:
    version = override_version or detect_version(target)
    return schema_path_for_version(version)


def install_guidance() -> str:
    return (
        "No validation backend is available. Install one of: "
        "xmllint (libxml2), Python package lxml, or Python package xmlschema."
    )


def parse_xmllint_errors(stderr: str) -> List[ValidationErrorItem]:
    errors: List[ValidationErrorItem] = []
    for line in stderr.splitlines():
        match = ERROR_PATTERN.search(line)
        if match:
            errors.append(
                ValidationErrorItem(
                    line=int(match.group("line")),
                    column=int(match.group("column")),
                    path=None,
                    message=match.group("message").strip(),
                    severity="error",
                )
            )
    if not errors and stderr.strip():
        errors.append(
            ValidationErrorItem(
                line=0,
                column=None,
                path=None,
                message=stderr.strip(),
                severity="error",
            )
        )
    return errors


def validate_with_xmllint(target: Path, schema: Path) -> object:
    result = run_command(["xmllint", "--noout", "--schema", str(schema), str(target)])
    if result.returncode == 0:
        return success_report("xmllint", as_posix_path(schema))
    return failure_report("xmllint", as_posix_path(schema), parse_xmllint_errors(result.stderr))


def validate_with_lxml(target: Path, schema: Path) -> object:
    from lxml import etree  # type: ignore

    schema_doc = etree.parse(str(schema))
    xmlschema = etree.XMLSchema(schema_doc)
    document = etree.parse(str(target))
    valid = xmlschema.validate(document)
    if valid:
        return success_report("lxml", as_posix_path(schema))

    errors: List[ValidationErrorItem] = []
    for entry in xmlschema.error_log:
        errors.append(
            ValidationErrorItem(
                line=entry.line or 0,
                column=getattr(entry, "column", None),
                path=getattr(entry, "path", None),
                message=entry.message,
                severity="error",
            )
        )
    return failure_report("lxml", as_posix_path(schema), errors)


def validate_with_xmlschema(target: Path, schema: Path) -> object:
    import xmlschema  # type: ignore

    validator = xmlschema.XMLSchema(str(schema))
    errors: List[ValidationErrorItem] = []
    for entry in validator.iter_errors(str(target)):
        errors.append(
            ValidationErrorItem(
                line=getattr(entry, "position", (0, None))[0] or 0,
                column=getattr(entry, "position", (0, None))[1],
                path=getattr(entry, "path", None),
                message=str(entry.reason or entry),
                severity="error",
            )
        )
    if not errors:
        return success_report("xmlschema", as_posix_path(schema))
    return failure_report("xmlschema", as_posix_path(schema), errors)


def validate(target: Path, schema: Path, backend: BackendInfo) -> object:
    if backend.name == "xmllint":
        return validate_with_xmllint(target, schema)
    if backend.name == "lxml":
        return validate_with_lxml(target, schema)
    if backend.name == "xmlschema":
        return validate_with_xmlschema(target, schema)
    raise UsageError(f"Unsupported backend: {backend.name}")


def print_human(report: object) -> None:
    if report.ok:
        print(f"VALID backend={report.backend} schema={report.schema}")
        return
    for error in report.errors:
        location = f"line={error.line}"
        if error.column is not None:
            location += f" column={error.column}"
        if error.path:
            location += f" path={error.path}"
        eprint(f"ERROR {location} message={error.message}")


def main() -> int:
    args = parse_args()
    if not args.target:
        raise UsageError("A target .rqml file is required")

    target = ensure_file(Path(args.target), "target document")
    schema = detect_schema(target, args.schema_version)
    backend = choose_backend()

    if backend is None:
        eprint(install_guidance())
        if args.json_output:
            report = failure_report(None, as_posix_path(schema), [
                ValidationErrorItem(
                    line=0,
                    column=None,
                    path=None,
                    message=install_guidance(),
                    severity="error",
                    suggestion="Install xmllint, lxml, or xmlschema",
                )
            ])
            print(report.to_json())
        return 2

    report = validate(target, schema, backend)
    if args.json_output:
        print(report.to_json())
    else:
        print_human(report)

    return 0 if report.ok else 1


if __name__ == "__main__":
    try:
        sys.exit(normalize_exit_code(main()))
    except UsageError as exc:
        eprint(str(exc))
        sys.exit(2)
