# ADR-0006: References mirror, not duplicate, the canonical RQML docs

- **Status**: Accepted
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-MIRROR`
- **Related requirements**: `REQ-AUTHORING-CRAFT`, `REQ-TOKEN-BUDGET`

## Context

The skill's `references/` directory needs to give an agent enough RQML domain knowledge to author and edit `.rqml` files correctly. The canonical version of this material already exists at `rqml.org/docs/`, which has comprehensive coverage of every element, attribute, and authoring pattern.

There are two ways to handle this overlap:

1. **Duplicate**: copy the relevant docs content into `references/`, keep both in sync.
2. **Mirror**: write agent-optimised condensations in `references/`, link to the canonical URL for full detail.

Duplication has the obvious drift problem: the skill's copy and the docs site will diverge whenever either is updated, and there is no signal that this has happened. It also doubles the maintenance burden — every doc change requires a parallel skill update — and discourages the skill maintainers from improving the canonical docs (because their own copy bears the cost of the change).

Mirroring solves drift by making the canonical version authoritative and the skill's version derivative. The trade-off is that the skill's content is necessarily smaller and more pointer-driven, which means agents can't rely on it alone for every edge case — they need to follow the link or invoke the canonical docs.

Agents have a different consumption pattern from humans. Humans browse, search, and back out; agents typically need a structured rule to apply *now*. So an agent-optimised condensation is not a worse version of the docs — it's a different artifact, optimised for a different reader.

## Decision

`references/elements/*.md` contains agent-optimised condensations of each RQML element's documentation. Each file:

- Begins with a one-line link to the canonical docs URL: `Canonical: https://rqml.org/docs/reference/elements/element-foo`.
- Lists required and optional attributes with one-line descriptions.
- Names the element's parent and child constraints.
- Includes a small valid example and one or two anti-pattern examples.
- Stays under 1500 tokens unless the element is genuinely complex.

`references/patterns.md`, `references/anti-patterns.md`, `references/strictness-levels.md`, `references/traceability-model.md`, and `references/workflow.md` are skill-original content that has no canonical counterpart. These are the genuinely additive parts of the skill.

A CI job verifies that every linked canonical URL resolves with HTTP 200 (broken-link check); it does not enforce content equivalence.

## Consequences

**Positive**
- No drift between skill and canonical docs by construction — the skill never tries to reproduce content authoritatively.
- Lower maintenance burden; canonical doc updates don't require skill updates unless the structure of the spec itself changes.
- Encourages improvements to the canonical docs because the skill maintainers benefit from them.
- The skill's reference content stays small enough to keep activation token costs manageable.

**Negative**
- Agents cannot work fully offline for edge cases that aren't covered in the local condensation; they may need network access to follow the canonical link. Acceptable because validation (the hot path) is already offline-safe per ADR-0002.
- Some duplication is unavoidable for the small examples shown in each element file; in practice these are short and the drift cost is negligible.
- A reader who doesn't follow the link may miss the full picture; mitigated by clear "see canonical" pointers at the top of each file.

## Alternatives considered

- **Full duplication with a sync script**: rejected because the sync script is itself a maintenance burden and never catches semantic drift, only textual drift.
- **No `references/` at all, link only to `rqml.org`**: rejected because it pushes too much load onto network access and gives the agent nothing to ground in offline.
- **Vendored copy of the docs site as a submodule**: rejected for the same drift reasons as full duplication, plus operational complexity.
