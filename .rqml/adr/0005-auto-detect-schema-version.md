# ADR-0005: Schema version is auto-detected from `rqml@version`

- **Status**: Superseded by [ADR-0008](0008-thin-skill-over-rqml-cli.md)
- **Date**: 2026-05-10
- **Decision ID** (in `requirements.rqml`): `DEC-AUTODETECT`
- **Related requirements**: `REQ-VERSION-DETECT`, `REQ-BUNDLE`

## Context

RQML has multiple schema versions in active use. As of May 2026:

- The latest GitHub release (`rqml-org/rqml`) is `RQML 2.0.1` (Jan 2026).
- The downloadable AGENTS.md template at `rqml.org/AGENTS.md` references schema `2.0.1`.
- The reference docs page at `rqml.org/docs/reference/` references schema `2.1.0`.
- The schema URL `rqml.org/schema/rqml-2.1.0.xsd` resolves and returns a real schema file.

Projects in the wild will be on different versions for different reasons:

- New projects copying from the docs site will start on 2.1.0.
- Projects copying from the GitHub README or AGENTS.md will start on 2.0.1.
- Long-lived projects will lag behind the latest version indefinitely.

The skill must validate every project's `.rqml` file against the *project's declared version*, not whichever version the skill author happens to think is current. Validating a 2.0.1 document against a 2.1.0 schema is wrong — features added or removed in 2.1.0 would produce false positives or false negatives.

## Decision

`scripts/validate.py` reads the document's `rqml@version` attribute and selects `references/schemas/rqml-{version}.xsd` as the validation schema. If the bundled directory does not contain a matching file, the script exits with a clear error naming the supported versions.

A `--schema-version VERSION` flag overrides the auto-detection, useful when testing migrations or validating partial documents.

The default for the `new_req.py` and template scaffolds is the latest bundled version, but this is a separate concern from validation.

## Consequences

**Positive**
- The skill works correctly for every project regardless of which version they're on.
- Adding support for a new RQML version is a matter of dropping a new XSD into `references/schemas/`; the dispatch logic is unchanged.
- Migration help is straightforward: validate against both old and new versions to identify what changes.
- Resolves the immediate 2.0.1/2.1.0 inconsistency in the published RQML materials cleanly — the skill simply respects whichever version the document declares.

**Negative**
- Maintaining test fixtures and CI runs across multiple bundled versions multiplies test surface.
- A user can cause confusion by changing `rqml@version` without migrating the document; the skill validates against the new version and reports apparent failures. Mitigated by emitting the chosen schema in the validation report so the cause is visible.
- `references/schemas/` grows over time; in practice this is a handful of files per year and not a real cost.

## Alternatives considered

- **Always validate against the latest bundled schema**: rejected because it produces wrong answers for projects on older versions and pressures projects into ad-hoc upgrades.
- **Require the user to pass `--schema-version` explicitly**: rejected because it adds friction to the dominant path (the document already declares its version) and creates a class of bugs where the flag and the document disagree.
- **Validate against the schema referenced by `xsi:schemaLocation` directly**: rejected because it would re-introduce a network dependency, breaking ADR-0002.
