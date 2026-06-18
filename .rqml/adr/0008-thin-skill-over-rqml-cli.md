# ADR-0008: Rewrite the skill as a thin SKILL.md skill over @rqml/cli

- **Status**: Accepted
- **Date**: 2026-06-18
- **Decision ID** (in `requirements.rqml`): `DEC-CLI-DELEGATION`
- **Related requirements**: `REQ-CLI-DELEGATION`, `REQ-NO-ENGINE`, `REQ-CLI-RUNTIME`, `REQ-PORTABLE`, `REQ-SKILL-MD`
- **Supersedes**: ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0007

## Context

The skill originally shipped a portable **Python engine** — `validate.py`,
`check_traces.py`, `lint.py`, `id_audit.py`, `matrix.py`, `extract.py` — plus
bundled XSDs and an `xmllint → lxml → xmlschema` fallback chain (ADR-0002, -0003,
-0004, -0005, -0007). When that was built, there was no published RQML toolchain
to lean on.

Since then the ecosystem went fully TypeScript. `@rqml/core` is the canonical
engine, published as `@rqml/cli` (and `@rqml/mcp`), and now covers validation,
referential integrity, lint, coverage, drift, trace, matrix, projection, and — as
of 0.6.0/0.7.0 — nearest-wins spec discovery, `--workspace` fan-out, and a `lint`
command. The skill's Python reimplemented a subset of this and had already drifted
from it — most visibly when a spec-file rename broke the skill's own `repo_root()`
discovery.

Two roles were tangled together in the skill: (a) a Python **engine**, and (b) a
**host-agnostic skill entry point**. Role (a) is now redundant and a maintenance /
drift liability. Role (b) is more valuable than ever: `SKILL.md` became an open
standard (Anthropic, Dec 2025) adopted by ~30–40 agents — Claude Code, Codex,
OpenCode, Cursor, Windsurf, Gemini CLI, GitHub Copilot, Cline, … — most of which
cannot load the host-specific `rqml-claude` / `rqml-codex` plugins. A portable
skill is the only way to reach them.

## Decision

Rewrite `rqml-skill` as a **thin, open-standard `SKILL.md` skill that delegates
all engine work to `@rqml/cli`**.

- Retire the Python engine: delete `scripts/` (the `*.py` engine and helpers),
  `references/schemas/` (bundled XSDs), and the validation-backend machinery.
- The skill becomes `SKILL.md` + `references/` that teach the five-stage process
  and drive `rqml` / `npx @rqml/cli` for every operation (validate, lint, check,
  status, show, impact, overview, matrix, link, approve, gate, skeleton, discover,
  `--workspace`).
- Correctness and offline operation are inherited from `@rqml/cli`, which bundles
  the canonical schema and runs offline. The skill states a minimum `@rqml/cli`
  version for the commands it documents.
- The spec file returns to the conventional name `requirements.rqml`.

Role (b) — the host-agnostic skill — is kept and sharpened; role (a) — the engine —
is retired.

## Consequences

**Positive**
- Zero engine duplication, so the skill can never drift from the canonical
  toolchain — it surfaces the toolchain's own output. This eliminates the
  schema-drift, false-pass, and version-skew risks that ADR-0002/0003/0005 existed
  to mitigate.
- Reaches the whole `SKILL.md` ecosystem, not only hosts with a dedicated plugin.
- Much less to maintain: no Python, no bundled schemas, no fallback chain, no
  weekly schema-provenance CI.

**Negative**
- Adds a hard dependency on `@rqml/cli` (Node), where the Python engine needed
  only Python. Mitigated by `npx @rqml/cli` and a clear in-skill install hint
  (RISK-CLI-MISSING).
- The skill must track a minimum `@rqml/cli` version for the commands it documents
  (RISK-CLI-VERSION).
- Loses pure-Python, no-Node portability — an accepted trade now that the
  ecosystem is TypeScript-first.

## Alternatives considered

- **Patch the Python engine** (fix `repo_root`, add nearest-wins discovery):
  rejected — keeps the duplication and the perpetual drift treadmill.
- **Retire the skill entirely** (rely on the Claude/Codex plugins + the CLI):
  rejected — leaves every other `SKILL.md`-compatible agent (OpenCode, Cursor, …)
  unserved.
- **A TS package importing `@rqml/core` directly**: rejected — duplicates the
  `@rqml/cli` surface for no gain; the agent interacts through the shell, where the
  CLI is the natural interface.

## Supersession

When accepted, this ADR supersedes ADR-0002 (bundle schemas), ADR-0003 (validation
fallback chain), ADR-0004 (Python scripts), ADR-0005 (auto-detect schema version),
and ADR-0007 (runtime strictness config) — all properties of the retired Python
engine, now owned by `@rqml/cli`. ADR-0001 (separate repo) and ADR-0006 (references
mirror the docs) remain in force.
