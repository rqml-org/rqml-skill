# Architecture Decision Records

This directory captures the major architecture and design decisions for the `rqml-skill` project. Each ADR is short, immutable once accepted, and follows the [Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html).

When a decision is revisited, do not edit the existing ADR — write a new one that supersedes it, and mark the older one as `Superseded by ADR-NNNN`.

## Index

| # | Title | Status |
|---|-------|--------|
| [0001](0001-skill-lives-in-its-own-repository.md) | Skill lives in its own repository under `rqml-org` | Accepted |
| [0002](0002-bundle-schemas-instead-of-fetching-them.md) | Bundle XSDs in the skill instead of fetching at runtime | Superseded by [0008](0008-thin-skill-over-rqml-cli.md) |
| [0003](0003-validation-tool-fallback-chain.md) | Validation uses an `xmllint → lxml → xmlschema` fallback chain | Superseded by [0008](0008-thin-skill-over-rqml-cli.md) |
| [0004](0004-python-as-script-language.md) | Scripts are written in Python 3.8+ | Superseded by [0008](0008-thin-skill-over-rqml-cli.md) |
| [0005](0005-auto-detect-schema-version.md) | Schema version is auto-detected from `rqml@version` | Superseded by [0008](0008-thin-skill-over-rqml-cli.md) |
| [0006](0006-mirror-rqml-docs-instead-of-duplicating.md) | References mirror, not duplicate, the canonical RQML docs | Accepted |
| [0007](0007-strictness-is-runtime-config.md) | Strictness level is read at runtime from project config | Superseded by [0008](0008-thin-skill-over-rqml-cli.md) |
| [0008](0008-thin-skill-over-rqml-cli.md) | Rewrite the skill as a thin SKILL.md skill over @rqml/cli | Accepted |

ADR-0008 supersedes ADR-0002, ADR-0003, ADR-0004, ADR-0005, and ADR-0007 (the retired Python-engine decisions), which are marked `Superseded by ADR-0008`. ADR-0001 (separate repo) and ADR-0006 (references mirror the docs) remain in force.

## Cross-reference

Each accepted decision is also captured as a `<decision>` element in `requirements.rqml` under `<catalogs><decisions>`, with the same identifier prefix (e.g. `DEC-REPO` ↔ ADR-0001). The `requirements.rqml` form is the agent-readable summary; this directory holds the long-form context.
