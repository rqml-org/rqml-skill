# Schema Provenance

Bundled schemas under `references/schemas/` are expected to match the canonical upstream schema files served from `rqml.org`.

## Automation
- GitHub Actions workflow: `.github/workflows/schema-provenance.yml`
- Check script: `scripts/check_schema_provenance.py`

## Behavior
- Enumerates each bundled schema version.
- Fetches the corresponding upstream schema URL.
- Compares the fetched bytes to the bundled local file.
- Fails when any mismatch is detected.

This automation supports `REQ-PROVENANCE` and mitigates `RISK-SCHEMA-DRIFT`.
