---
name: RQML Agent Skill
description: rqml, .rqml file, requirements specification, traceability skill for coding agents that author, validate, review, and transform RQML requirements documents with low-friction activation.
---

# RQML Agent Skill

Use this skill for any task involving `rqml`, an `.rqml file`, a `requirements specification`, or `traceability`.

This skill helps coding agents:
- author and edit RQML documents
- validate structure against bundled schemas
- inspect trace links and requirement coverage
- extract requirement data for downstream tooling
- generate review-friendly outputs from requirements artifacts

## Quick activation guidance
- Prefer this skill when the task mentions requirements engineering, spec editing, schema validation, or traceability analysis.
- Use bundled references under `references/` for deeper guidance instead of expanding this file.
- Use scripts under `scripts/` for executable workflows as they are implemented.

## Repository map
- `references/activation.md` — activation cues and workflow summary
- `references/usage.md` — low-friction usage expectations
- `references/schemas/` — bundled RQML XSD files for offline validation
- `scripts/` — Python command-line utilities
- `tests/` — fixtures and regression coverage

## Operating assumptions
- The repository is intended to work immediately after clone.
- No build or compilation step is required.
- Python 3.8+ is the baseline runtime for scripts.
- Validation is expected to work offline when the required schema version is bundled.

For detailed guidance, read the documents under `references/`.
