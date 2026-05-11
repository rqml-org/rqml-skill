# Implementation Plan

## Stage 1 — Bootstrap skill repository skeleton
- [x] **Scope:** REQ-LAYOUT, REQ-LICENSE
- [x] **Agent task:** Create the initial repository structure and baseline project files for a no-build Python skill repository.
- [x] **Touch files/modules:** `SKILL.md`, `LICENSE`, `scripts/`, `references/`, `references/schemas/`, `assets/`, `tests/`, `tests/fixtures/`, optional `.gitignore`, optional `scripts/requirements.txt`
- [x] **Inputs needed:** `requirements` package `PKG-SKILL`, `PKG-LICENSING`; `catalogs/constraints` (`CON-LICENSE`); ADRs 0001, 0002, 0004
- [x] **Key output:** Repository layout and Apache-2.0 licensing baseline ready for implementation
- [x] **Verify:** Confirm required directories/files exist; run basic file-tree check; ensure no build tooling is required

## Stage 2 — Author SKILL.md for agent activation
- [x] **Scope:** REQ-SKILL-MD, REQ-TRIGGERS, REQ-TOKEN-BUDGET, REQ-NO-INSTALL
- [x] **Agent task:** Write a compliant `SKILL.md` with valid YAML frontmatter, front-loaded trigger phrases, concise activation guidance, and references to detailed docs under `references/`.
- [x] **Touch files/modules:** `SKILL.md`, supporting docs under `references/`
- [x] **Inputs needed:** `requirements` in `PKG-SKILL` and `PKG-PLATFORM`; `goals` `GOAL-LOW-FRICTION`; `qgoals` `QGOAL-FAST-ACTIVATION`; constraints `CON-AGENTSKILLS`, `CON-TOKEN-BUDGET`
- [x] **Key output:** Production-ready `SKILL.md` that is discoverable by coding agents and stays within token/line budget
- [x] **Verify:** Run Agent Skills validator if available; check presence of required frontmatter fields and trigger phrases; confirm body stays under 5000 tokens and 500 lines

## Stage 3 — Bundle supported RQML schemas and fixtures
- [x] **Scope:** REQ-BUNDLE, REQ-OFFLINE
- [x] **Agent task:** Add bundled XSD files for supported schema versions and create valid/invalid fixture documents for offline validation workflows.
- [x] **Touch files/modules:** `references/schemas/rqml-2.0.1.xsd`, `references/schemas/rqml-2.1.0.xsd`, `tests/fixtures/valid-2.0.1.rqml`, `tests/fixtures/valid-2.1.0.rqml`, `tests/fixtures/invalid-missing-version.rqml`
- [x] **Inputs needed:** `requirements` in `PKG-VALIDATE`; `scenarios` `SCN-OFFLINE`, `SCN-OLD-SCHEMA`; ADRs 0002, 0005
- [x] **Key output:** Offline schema bundle and baseline fixtures for validation tests
- [x] **Verify:** Confirm schema files exist at the expected paths; inspect fixture versions and intentional invalid case; ensure no runtime fetch is required

## Stage 4 — Implement shared Python validation core
- [x] **Scope:** REQ-PYTHON, REQ-PLATFORM
- [x] **Agent task:** Build shared Python utilities for path handling, XML parsing, backend selection, result normalization, and cross-platform CLI behavior to support all scripts.
- [x] **Touch files/modules:** `scripts/_common.py`, `scripts/_xml.py`, `scripts/_backends.py`, `scripts/_report.py`, optional `tests/test_common.py`
- [x] **Inputs needed:** `domain/entities` (`ENT-RQMLDOC`, `ENT-XSD`, `ENT-VALERR`); `requirements` in `PKG-PLATFORM`; ADRs 0003, 0004, 0007
- [x] **Key output:** Reusable Python 3.8+ support layer used by all command-line scripts
- [x] **Verify:** Run unit tests for path/process handling on current platform; run syntax check with Python 3.8+; confirm only stdlib plus optional accelerators are assumed

## Stage 5 — Implement XSD validation CLI
- [x] **Scope:** REQ-XSD-VALIDATE, REQ-FALLBACK, REQ-VERSION-DETECT, REQ-JSON-OUT, REQ-OFFLINE
- [x] **Agent task:** Implement `scripts/validate.py` with version auto-detection, `--schema-version` override, backend fallback chain (`xmllint -> lxml -> xmlschema`), normalized error reporting, and `--json` output.
- [x] **Touch files/modules:** `scripts/validate.py`, shared modules from Stage 4, optional `tests/test_validate.py`
- [x] **Inputs needed:** `requirements` in `PKG-VALIDATE`; `verification` test cases `TC-VALID`, `TC-INVALID-MISSING`, `TC-FALLBACK`, `TC-NO-TOOL`, `TC-OLD-SCHEMA`, `TC-OFFLINE`, `TC-PERFORMANCE`; ADRs 0002, 0003, 0005
- [x] **Key output:** Cross-platform validation command that selects the correct bundled schema and emits human-readable and JSON reports
- [x] **Verify:** Run `scripts/validate.py` against valid and invalid fixtures; test backend fallback by masking tools; test `--json`; confirm exit codes 0/1/2 match spec; confirm offline execution with no network dependency

## Stage 6 — Implement semantic lint with runtime strictness
- [x] **Scope:** REQ-LINT
- [x] **Agent task:** Implement `scripts/lint.py` to enforce semantic checks by strictness level, reading project strictness from `.rqml-skill.yaml` or `AGENTS.md` and reporting failures clearly.
- [x] **Touch files/modules:** `scripts/lint.py`, `scripts/_strictness.py`, optional `.rqml-skill.yaml` example, `tests/test_lint.py`, `tests/fixtures/` lint cases
- [x] **Inputs needed:** `requirements` `REQ-LINT`; `risks` `RISK-FALSE-PASS`; decision `DEC-STRICTNESS`; ADR 0007
- [x] **Key output:** Strictness-aware semantic linter for acceptance-criteria and trace metadata policies
- [x] **Verify:** Run lint in standard/strict/certified modes against targeted fixtures; confirm rule activation changes by mode; ensure non-zero exit on violations

## Stage 7 — Implement trace target resolver
- [x] **Scope:** REQ-TRACE-CHECK
- [x] **Agent task:** Implement `scripts/check_traces.py` to resolve `doc` locators against local files and `external` locators against HTTP/URI targets, reporting unresolved references and actionable diagnostics.
- [x] **Touch files/modules:** `scripts/check_traces.py`, optional shared trace helpers `scripts/_trace.py`, `tests/test_check_traces.py`, trace fixtures
- [x] **Inputs needed:** `requirements` `REQ-TRACE-CHECK`; `risks` `RISK-FALSE-PASS`; `trace` section structure in spec
- [x] **Key output:** Trace resolution utility for non-local trace endpoints
- [x] **Verify:** Run against fixtures containing valid and invalid `doc`/`external` locators; confirm unresolved targets are reported; verify local-filesystem resolution works without modifying network-independent core behavior

## Stage 8 — Implement ID audit tooling
- [x] **Scope:** REQ-ID-AUDIT
- [x] **Agent task:** Implement `scripts/id_audit.py` to detect duplicate IDs, naming-pattern violations, and ID changes versus previous git revision.
- [x] **Touch files/modules:** `scripts/id_audit.py`, optional `scripts/_git.py`, `tests/test_id_audit.py`, git-aware fixtures or temp repo harness
- [x] **Inputs needed:** `requirements` `REQ-ID-AUDIT`; `meta/conventions` if added later; current spec ID conventions from schema guidance
- [x] **Key output:** CLI audit tool for identifier hygiene and change tracking
- [x] **Verify:** Run against fixtures with duplicate and malformed IDs; run in a temporary git repo to confirm previous-version comparison behavior; verify graceful handling when git history is unavailable

## Stage 9 — Implement requirement extraction CLI
- [x] **Scope:** REQ-EXTRACT
- [x] **Agent task:** Implement `scripts/extract.py` to parse requirements and emit the specified JSON array schema for downstream agent tooling.
- [x] **Touch files/modules:** `scripts/extract.py`, shared XML helpers, `tests/test_extract.py`
- [x] **Inputs needed:** `requirements` `REQ-EXTRACT`; RQML `requirements` section and `ReqTypeItem` structure from spec/schema
- [x] **Key output:** Machine-readable requirement export utility
- [x] **Verify:** Run against `requirements.rqml` and fixtures; validate JSON shape contains `id`, `type`, `title`, `priority`, `status`, `statement`; ensure stable output ordering

## Stage 10 — Implement traceability matrix generator
- [x] **Scope:** REQ-MATRIX
- [x] **Agent task:** Implement `scripts/matrix.py` to emit a Markdown matrix of requirements and grouped trace relationships (`satisfies`, `dependsOn`, `mitigates`, `verifiedBy`).
- [x] **Touch files/modules:** `scripts/matrix.py`, shared trace helpers, `tests/test_matrix.py`
- [x] **Inputs needed:** `requirements` `REQ-MATRIX`; `scenario` `SCN-MATRIX`; `verification` `TC-MATRIX`; current `trace` section in spec
- [x] **Key output:** Markdown traceability matrix suitable for PR descriptions and reviews
- [x] **Verify:** Run against `requirements.rqml` and fixture docs; confirm one row per requirement and grouped trace columns; compare stdout against expected snapshot

## Stage 11 — Add provenance CI automation
- [x] **Scope:** REQ-PROVENANCE
- [x] **Agent task:** Implement CI workflow and supporting script to fetch upstream schemas on a schedule, diff against bundled copies, and fail on mismatch.
- [x] **Touch files/modules:** `.github/workflows/schema-provenance.yml`, `scripts/check_schema_provenance.py` or similar, optional CI docs in `references/`
- [x] **Inputs needed:** `requirements` `REQ-PROVENANCE`; `risks` `RISK-SCHEMA-DRIFT`; `verification` `TC-PROVENANCE`; ADR 0002
- [x] **Key output:** Automated weekly schema provenance check that blocks releases on drift
- [x] **Verify:** Run script locally with mocked responses if possible; validate CI workflow syntax; confirm mismatch produces failing exit code

## Stage 12 — Complete self-test suite and performance verification
- [x] **Scope:** TC-VALID, TC-INVALID-MISSING, TC-FALLBACK, TC-NO-TOOL, TC-OLD-SCHEMA, TC-OFFLINE, TC-MATRIX, TC-AGENTSKILLS, TC-PROVENANCE, TC-PERFORMANCE
- [x] **Agent task:** Build the full automated test harness, including integration tests for script CLIs, backend-selection scenarios, offline behavior, and performance checks for validation latency.
- [x] **Touch files/modules:** `tests/`, `tests/fixtures/`, test runner config if needed, optional helper scripts for fixture generation
- [x] **Inputs needed:** `verification` section; all implemented scripts; `qgoal` `QGOAL-FAST-VALIDATE`
- [x] **Key output:** End-to-end regression suite covering required validation, matrix, provenance, and performance behavior
- [x] **Verify:** Run all tests; run performance test on 2000-line fixture; confirm expected exit codes, stdout/stderr formats, and latency target for xmllint/lxml paths

## Readiness Verdict
**NOT READY**

### Blockers
- [ ] No implementation code exists yet; workspace currently contains the spec and ADRs only
- [x] No `.rqml/plan.md` implementation tracker exists in the repository
- [ ] No source files, bundled schemas, fixtures, CI workflows, or tests are present yet
- [ ] Some verification steps depend on external tooling or environments being available during execution (`xmllint`, optional `lxml`/`xmlschema`, Agent Skills validator, CI network access for provenance checks)
