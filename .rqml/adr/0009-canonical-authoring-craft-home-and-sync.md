# ADR-0009: rqml-skill is the canonical home for RQML authoring craft, synced to the plugins

- **Status**: Accepted
- **Date**: 2026-06-19
- **Decision ID** (in `requirements.rqml`): `DEC-CRAFT-HOME`
- **Related requirements**: `REQ-AUTHORING-CRAFT`, `REQ-CRAFT-SYNC`
- **Refines**: ADR-0008 (thin skill over @rqml/cli)

## Context

RQML authoring craft — the eleven-section model, statement-quality rules, the
type taxonomy, ID conventions, the lifecycle ladder, traceability rules — was
independently re-expressed in rqml-claude (a rich ~65-line guide) and rqml-codex
(a slim checklist) and had diverged, with no single canonical home. ADR-0008 made
SKILL.md deliberately thin and pushed detail into `references/`, but the craft
itself was never given a home in rqml-skill — it lived only inside the plugins.

The plugins cover Claude Code and Codex natively; rqml-skill reaches every other
skills-compatible host. We want one source of truth for the craft, available
**offline and in-context inside the plugins** (not only behind a web link), kept
current without manual copying.

## Decision

Make rqml-skill the canonical, host-agnostic home for the authoring craft,
delivered as `references/authoring.md`. SKILL.md stays thin (ADR-0008) and points
to it; this honors DEC-MIRROR — the reference is an agent-optimized condensation
that still links to the rqml.org docs.

The plugins **vendor** a synced copy of `references/authoring.md` (at
`skills/rqml-authoring/authoring.md`) for offline, in-context use rather than
re-expressing the craft. rqml-skill provides an automated sync
(`.github/workflows/sync-craft.yml`) that opens a refresh pull request on each
plugin when the reference changes; each plugin runs a CI drift guard that fails
if its vendored copy diverges from the canonical. The reference carries a
`canonical-version` stamp that the sync and guard track.

## Consequences

**Positive**
- One source of truth for the craft; the plugins' own authoring skills slim to
  host specifics plus a pointer to the vendored reference.
- Craft stays available offline and in-context in each plugin.
- Updates propagate automatically — a single rqml-skill PR fans out to refresh
  PRs on both plugins.

**Negative**
- A standing automation to maintain.
- A cross-repo write credential (`CRAFT_SYNC_TOKEN`) must be provisioned for the
  rqml-org organization; until it is, the sync workflow no-ops with a warning.
- A brief drift window between an upstream change and the merged sync PR, bounded
  by the plugin-side drift guard.

## Alternatives considered

- **Link-out only** (plugins reference rqml.org/docs, no copy): rejected — loses
  the offline, in-context craft inside the plugins.
- **Manual vendoring** (copy by hand on each change): rejected — drifts and
  relies on discipline.
- **Keep three independent expressions**: rejected — the divergence this ADR
  exists to end.
