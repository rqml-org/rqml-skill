# ADR-0002: Bundle XSDs in the skill instead of fetching at runtime

- **Status**: Superseded by [ADR-0008](0008-thin-skill-over-rqml-cli.md)
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-BUNDLE`
- **Related requirements**: `REQ-BUNDLE`, `REQ-OFFLINE`, `REQ-PROVENANCE`

## Context

XSD validation needs an XSD. Two approaches are possible:

1. **Fetch on demand**: `validate.py` resolves `https://rqml.org/schema/rqml-{version}.xsd` at runtime.
2. **Bundle**: ship every supported schema version inside `references/schemas/` and dispatch locally.

Agent skills run in a wide variety of environments. Some are sandboxed without network egress (Claude Code's agent tier, GitHub Copilot's enterprise modes, Codex CLI in containerised CI). Some have intermittent connectivity. All of them invoke validation many times per session — typically after every edit — which means even a 200ms fetch becomes a real latency drag.

There is also a trust dimension: a runtime fetch means the validation result depends on a remote server's availability and integrity. A skill whose validity depends on `rqml.org` being reachable and unmodified is structurally fragile.

The cost of bundling is small: each schema is a single XSD file, expected to be under 100 KB even at maximum complexity. Bundling all reasonable historical versions is cheap on disk and free at activation time (the SKILL.md stays small; schemas only load when validation actually runs).

## Decision

Bundle every supported schema version under `references/schemas/rqml-{version}.xsd`. `validate.py` resolves schemas locally; it never makes network calls.

To prevent silent drift between bundled and upstream schemas, a CI job runs weekly:

1. Fetches each schema from `rqml.org`.
2. Diffs it byte-for-byte against the bundled copy.
3. Fails the build on any diff, blocking the next release until either the bundle is updated or the upstream change is reviewed and accepted.

This is captured as `REQ-PROVENANCE` and verified by `TC-PROVENANCE`.

## Consequences

**Positive**
- Validation works in fully offline environments, which is increasingly the default for agent runtimes.
- Latency is bounded by the local file system, not the network.
- The skill's behaviour is deterministic and version-pinned.
- Validation results don't depend on `rqml.org` uptime.

**Negative**
- Bundled schemas can drift from upstream; mitigated by the weekly CI provenance check.
- The skill repo grows linearly in supported versions; acceptable at the scale of a typical spec lifecycle (single-digit versions per year).
- Adding a new RQML version requires a skill release, not just a server-side change at `rqml.org`.

## Alternatives considered

- **Always fetch with a local cache**: rejected because the first invocation still requires network, breaking the offline guarantee, and cache invalidation rules add complexity for marginal benefit.
- **Bundle only the latest, fetch older versions**: rejected because the AGENTS.md template currently still references 2.0.1 while the docs site references 2.1.0, so projects in the wild use both — the skill needs to handle both reliably without network.
