# ADR-0007: Strictness level is read at runtime from project config

- **Status**: Accepted
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-STRICTNESS`
- **Related requirements**: `REQ-LINT`

## Context

RQML's AGENTS.md defines four strictness levels (`relaxed`, `standard`, `strict`, `certified`) that determine how aggressively an agent enforces spec-first development:

| Level | Spec-first? | Code traces | Test traces | Ghost features |
|-------|-------------|-------------|-------------|----------------|
| `relaxed` | recommended | optional | optional | allowed |
| `standard` | required | new features | new reqs | blocked |
| `strict` | required | all changes | all reqs | blocked |
| `certified` | approved-first | with metadata | full matrix | blocked |

These levels affect what the skill's semantic linter (`scripts/lint.py`) should flag. Under `standard`, every requirement should have acceptance criteria. Under `strict`, every change to a requirement should produce a trace edge. Under `certified`, trace edges must carry `createdBy`, `createdAt`, and `confidence` metadata.

The XSD does not encode these rules — they're project-policy layered on top of structural validity. The lint script needs to know which level applies for a given project.

Two ways to handle this:

1. **Bake strictness into the skill**: ship one default and require lint flags to override.
2. **Read strictness at runtime from the project**: the skill discovers the level on every invocation.

The first option is simpler but wrong: different projects in different agent sessions can have different strictness, and a globally-configured skill can't track that. The second option requires defining where the level lives, but matches the existing AGENTS.md convention naturally — AGENTS.md already declares the level in plain text at the top.

## Decision

`scripts/lint.py` resolves the strictness level on each invocation in the following order:

1. **`--strictness LEVEL` command-line flag** (highest priority, for ad-hoc overrides).
2. **`.rqml-skill.yaml`** in the project root, if present, with a top-level `strictness:` key.
3. **`AGENTS.md`** in the project root, parsed with a small regex to extract the line `## Strictness: \`<level>\`` documented in the canonical AGENTS.md template.
4. **Default to `standard`** if none of the above are found.

The chosen level is reported in the lint output so its origin is visible.

The `.rqml-skill.yaml` file is optional and intentionally minimal — most projects should rely on AGENTS.md to avoid drift between strictness declarations.

## Consequences

**Positive**
- One skill installation correctly handles every project regardless of its strictness.
- Reuses the AGENTS.md convention that already exists, so most projects need no extra configuration.
- The escape hatch of `.rqml-skill.yaml` covers projects that don't use AGENTS.md or want skill-specific config separated.
- Agents can override per-task with `--strictness` for short-lived experiments.

**Negative**
- AGENTS.md parsing is lightly regex-based, which is fragile if the template format changes; mitigated by treating `## Strictness: \`<level>\`` as a stable contract documented in the upstream AGENTS.md.
- Two configuration sources can disagree (AGENTS.md says one thing, `.rqml-skill.yaml` says another); resolved deterministically by the priority order above and surfaced in lint output.
- A project that forgets to declare a strictness level silently gets `standard`; this is the right default but should be made explicit in skill output.

## Alternatives considered

- **Single global default, configured per skill installation**: rejected because the same agent installation will work on multiple projects with different strictness needs.
- **Read strictness from the `.rqml` file itself**: rejected because the strictness level is a project-policy concern, not a document-level one, and embedding it in every requirements document creates noise. There is no existing element in the RQML schema to hold it cleanly.
- **Always require an explicit `--strictness` flag**: rejected because it adds friction for the dominant path and doesn't match the AGENTS.md convention agents already have to read for other reasons.
