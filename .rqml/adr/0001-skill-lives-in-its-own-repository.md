# ADR-0001: Skill lives in its own repository under `rqml-org`

- **Status**: Accepted
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-REPO`
- **Related requirements**: `REQ-LAYOUT`, `REQ-LICENSE`

## Context

There are three plausible homes for the RQML agent skill:

1. **In the spec repo** at `github.com/rqml-org/rqml`, alongside the XSD and AGENTS.md template, surfaced through `rqml.org`.
2. **In the toolset repo** at `rqml.dev`, alongside the VS Code extension.
3. **In its own repository** under the `rqml-org` GitHub organisation.

Each has trade-offs. Option 1 carries authority (the skill is unambiguously canonical) but blurs the standards/implementation boundary that mature specs (LSP, JSON Schema, MCP) keep clean. Option 2 keeps tools together and simplifies coordinated releases but under-positions the skill — it has a different audience (Cursor/Codex/Claude Code users rather than VS Code users) and a much wider distribution surface than the extension. Option 3 matches what most ecosystem players do (Stripe, Atlassian, Figma, Notion all ship their skills from dedicated places), but introduces fragmentation risk if cross-linking is sloppy.

The skill is also expected to be PR'd into community skills directories like `anthropics/skills` and `awesome-copilot`, which expects a clean top-level repo URL rather than a path inside a tooling monorepo.

## Decision

Host the skill in a dedicated repository at `github.com/rqml-org/rqml-skill`.

Discoverability is handled by:

- A prominent link from `rqml.org` describing the skill as the canonical agent integration.
- Listing the skill among tools at `rqml.dev`.
- Submission to relevant community skills directories.

Drift between the three URLs is mitigated by:

- A `rqml-spec: 2.x.y` declaration in the skill's `VERSION` file, so consumers can see at a glance which spec revision a given skill release targets.
- A README that names this repository as the canonical reference skill maintained by the RQML maintainers.

## Consequences

**Positive**
- Clean clone URL for distribution and submission to skills directories.
- Independent release cadence from both the spec and the VS Code extension.
- Different contributors and reviewers can own the skill without spec governance overhead.
- The spec repository stays implementation-free, preserving long-term governance hygiene.

**Negative**
- Three URLs to keep in sync (`rqml.org`, `rqml.dev`, `github.com/rqml-org/rqml-skill`).
- Lockstep versioning with the spec is no longer free; `VERSION` and CI must enforce it.
- Discovery requires deliberate cross-linking; without it, the skill becomes orphaned.

## Alternatives considered

- **Spec repo**: rejected for governance reasons; conflates "what RQML is" with "how this skill thinks about RQML".
- **Toolset monorepo**: rejected because the URL `github.com/rqml-org/toolset/skills/rqml` is awkward to distribute and bundles the skill with a product (the VS Code extension) it has no shared audience with.
