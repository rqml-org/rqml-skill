# ADR-0003: Validation uses an `xmllint → lxml → xmlschema` fallback chain

- **Status**: Superseded by [ADR-0008](0008-thin-skill-over-rqml-cli.md)
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-FALLBACK`
- **Related requirements**: `REQ-FALLBACK`, `REQ-XSD-VALIDATE`

## Context

XSD 1.0 validation is supported by several tools, none of which are universally available in agent environments:

- **xmllint** (libxml2 native binary): preinstalled on macOS, ships in `libxml2-utils` on Debian/Ubuntu, available on Windows via libxml2 builds. Fast, authoritative for XSD 1.0, but not always on `PATH`.
- **lxml** (Python library, libxml2 bindings): widely installed in Python environments because of pandas, BeautifulSoup, and other downstream consumers, but not in the standard library.
- **xmlschema** (pure-Python library): no native dependencies, supports XSD 1.0 and 1.1, slower than libxml2-based options. Easy to install everywhere Python runs.

Picking one and forcing it on users would either (a) require a `pip install` step in environments that already have a working validator, violating `REQ-NO-INSTALL`, or (b) miss the fastest available option.

## Decision

`scripts/validate.py` tries each backend in priority order and uses the first that succeeds:

1. **xmllint** (subprocess) — chosen first because it's the most commonly preinstalled, the fastest, and the canonical reference implementation cited in RQML's own AGENTS.md.
2. **lxml** (Python import) — chosen second because it shares libxml2 with xmllint, so behaviour is consistent, but works inside Python without a subprocess and without xmllint being on `PATH`.
3. **xmlschema** (Python import) — chosen third as the last-resort pure-Python option that requires no native dependencies.

If all three fail to load, `validate.py` exits with code `2` (distinct from `1` = invalid document) and prints installation guidance for all three options. This gives the agent something actionable rather than a generic failure.

The chosen backend is reported in the validation output (both human-readable and JSON modes) so users can debug performance issues or reproducibility problems.

## Consequences

**Positive**
- Works out of the box in macOS, most Linux distributions, and standard Python environments without extra installation.
- `REQ-NO-INSTALL` holds: a fresh `git clone` is immediately usable in the common case.
- Performance is preserved by trying the fastest backend first.
- When validation fails for environmental reasons (no backend), the agent gets a clear, actionable error rather than a confusing one.

**Negative**
- Three code paths to maintain and test instead of one.
- Subtle differences between backends are possible (xmllint and lxml share libxml2, but xmlschema is a separate implementation); fixtures need to be exercised against all three in CI.
- The first run pays a small cost to detect which backend is available; this is amortised across subsequent calls.

## Alternatives considered

- **Force `pip install lxml`**: rejected because it violates `REQ-NO-INSTALL` and adds friction for the common case where xmllint is already present.
- **Bundle a static xmllint binary per platform**: rejected because cross-platform binary distribution is operationally heavy for marginal benefit, and Python is already a hard dependency.
- **Single-backend (xmllint only)**: rejected because Windows environments without libxml2 in `PATH` are common in CI and would fail.
