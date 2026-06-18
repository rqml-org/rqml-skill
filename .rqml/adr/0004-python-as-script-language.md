# ADR-0004: Scripts are written in Python 3.8+

- **Status**: Superseded by [ADR-0008](0008-thin-skill-over-rqml-cli.md)
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-PYTHON`
- **Related requirements**: `REQ-PYTHON`, `REQ-PLATFORM`

## Context

The skill's executable services (`validate.py`, `check_traces.py`, `lint.py`, `id_audit.py`, `matrix.py`, `extract.py`, `new_req.py`) need a runtime that satisfies several constraints simultaneously:

- Available in essentially every agent environment without installation.
- Cross-platform across macOS, Linux, and Windows.
- Has good XML and XSD libraries (`lxml`, `xmlschema`).
- Familiar enough to maintainers and contributors that the codebase doesn't fragment.
- Stable across at least the next several years of agent runtime evolution.

Realistic candidates are Python, Bash, and Node.js.

**Bash** has the lowest install footprint on Unix-like systems but fails the cross-platform test (Windows requires WSL or Git Bash, neither guaranteed in agent runtimes), has no native XSD validation, and forces shelling out to `xmllint` for everything — losing the lxml and xmlschema fallbacks entirely.

**Node.js** is widely installed but XSD support is poor — `libxmljs` is the main option and has historically had native-binding fragility on macOS ARM and Windows. Its standard library is also less amenable to scripting tasks like XML manipulation than Python's.

**Python** is preinstalled on macOS and most Linux distributions, available on Windows via the official installer (and bundled in many agent runtimes), has first-class XML support in the standard library, and provides both `lxml` and `xmlschema` as widely-used XSD libraries.

The minimum version to support is the question. Python 3.8 introduced f-strings with `=`, walrus operator, and structural improvements that simplify the code, while remaining available in essentially every still-supported OS distribution as of 2026. Going lower (3.7 or 3.6) costs maintainability for negligible reach gain. Going higher (3.10+) excludes some long-running CI environments and stable-channel distros.

## Decision

All scripts target Python 3.8 or later. Scripts use only the standard library plus optional acceleration via `lxml` or `xmlschema` (handled transparently by the fallback chain in ADR-0003).

A `scripts/requirements.txt` lists the optional packages but is not required for the skill to function — `lxml` and `xmlschema` are listed there for users who want to install them explicitly, but the validation fallback chain handles their absence.

Each script begins with `#!/usr/bin/env python3` and includes a `--help` flag.

## Consequences

**Positive**
- Cross-platform with no per-platform code paths.
- Standard library handles XML parsing, JSON output, subprocess management, and filesystem operations without external dependencies.
- `lxml` and `xmlschema` both happen to be Python libraries, so they integrate naturally into the same scripts.
- Wide contributor pool; Python is one of the most common languages for skill authoring.

**Negative**
- Adds Python as a hard dependency for projects that don't otherwise have it (rare in agent environments, but possible).
- Python startup latency (~50-150ms) is non-trivial for very small scripts; acceptable given the skill's scripts are not in performance-critical loops.
- Python 3.8 sets a soft floor for some modern syntax features (e.g. `match` statements from 3.10).

## Alternatives considered

- **Bash with awk/sed**: rejected for Windows incompatibility and lack of XSD validation.
- **Node.js**: rejected for weaker XSD ecosystem and worse cross-platform stability of native bindings.
- **Go binaries (precompiled)**: rejected for distribution complexity and platform-binary management; not worth it for scripts that mostly orchestrate `xmllint` and parse XML.
- **Python 3.6 or 3.7**: rejected for marginal reach gain at clear maintainability cost.
