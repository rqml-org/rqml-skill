# Test Suite Overview

This directory contains unit and integration-style regression tests for the RQML skill scripts.

## Coverage themes
- Validation CLI structure, fallback handling, and schema dispatch
- Semantic lint by strictness level
- Trace resolution for local doc and external locators
- ID audit and git-aware comparison behavior
- Requirement extraction
- Traceability matrix generation
- CLI-level smoke tests across implemented commands
- Lightweight performance guard for validation latency on fixtures

## Notes
- Some tests accept environment-dependent exit codes where optional backends or network access may be unavailable.
- Provenance and Agent Skills verification remain partly environment-dependent and are better exercised in CI.
