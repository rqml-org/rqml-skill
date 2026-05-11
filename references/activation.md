# Activation Guide

Use the RQML Agent Skill when a task involves `.rqml` files, requirements specifications, traceability analysis, requirement extraction, or validation of RQML documents.

## Primary workflows
- Validate an RQML document with `scripts/validate.py`
- Inspect traceability relationships with `scripts/matrix.py`
- Run semantic checks with `scripts/lint.py`
- Extract requirement data for downstream tooling with `scripts/extract.py`

## Activation cues
Activate this skill when the prompt mentions:
- `rqml`
- `.rqml file`
- `requirements specification`
- `traceability`
- schema validation
- requirement coverage

## Repository layout
- `SKILL.md` — compact activation entrypoint for agent hosts
- `references/` — supporting guidance and bundled schemas
- `scripts/` — executable tooling
- `tests/` — fixtures and regression coverage
