# RQML Agent Skill

Bring **RQML** into your coding-agent workflow in minutes.

The **RQML Agent Skill** helps coding agents author, validate, lint, review, and transform `.rqml` requirements specifications so your team can work in a more disciplined **spec-first** way without adding a heavy setup burden.

If you want agents to do more than “edit some XML” — and instead reliably work with requirements, traceability, acceptance criteria, and validation — this repository gives them the right entry point.

## Why install this skill

Teams adopt this skill because it makes agent-assisted requirements work more practical:

- **Faster onboarding** — agents get a clear `SKILL.md` entry point and purpose-built references
- **Less ambiguity** — agents are nudged toward the five-stage [spec → design → plan → code → verify](https://rqml.org/docs/development-process) process
- **Better validation** — bundled schemas and validation tooling reduce guesswork
- **Better traceability** — requirements, goals, scenarios, tests, and implementation stay easier to connect
- **Low friction** — no build step is required for normal use
- **Offline-friendly** — core validation workflows can run without network access

## Getting started

### 1. Install the skill

Clone or copy this repository into the skills directory used by your coding agent host.

The exact location depends on the host, but the core idea is simple: the agent needs access to this repository so it can discover `SKILL.md` and the supporting files in this project.

Once installed, restart or refresh your agent environment if needed.

### 2. Confirm the key files are present

At minimum, this repository should contain:

- `SKILL.md` — the activation entry point for the agent
- `references/` — compact supporting docs for agent guidance
- `references/schemas/` — bundled RQML schema files
- `scripts/` — command-line tools for validation and analysis
- `requirements.rqml` — this project’s own RQML specification

### 3. Activate it with the right kind of task

This skill is meant to activate when your task involves things like:

- `rqml`
- `.rqml files`
- requirements specifications
- traceability
- acceptance criteria
- schema validation
- requirements review

Examples:

- “Validate this `.rqml` file and explain the errors.”
- “Add a new requirement and acceptance criteria to this requirements specification.”
- “Generate a traceability matrix from this RQML document.”
- “Check whether these requirements have proper verification coverage.”

### 4. Run validation

The fastest way to get value from the repository is to validate an RQML document.

```bash
python scripts/validate.py requirements.rqml
```

For machine-readable output:

```bash
python scripts/validate.py --json requirements.rqml
```

### 5. Run semantic checks

After structural validation, run linting and trace-related checks.

```bash
python scripts/lint.py requirements.rqml
python scripts/check_traces.py requirements.rqml
python scripts/id_audit.py requirements.rqml
```

### 6. Generate useful outputs

For downstream tooling or review workflows:

```bash
python scripts/extract.py requirements.rqml
python scripts/matrix.py requirements.rqml
```

## What you get

This repository gives agents and developers a lightweight but practical toolbelt for RQML work.

### Agent activation and guidance

`SKILL.md` is designed to help compatible coding agents quickly recognize relevant tasks and load just enough context to act usefully.

Detailed material is kept under `references/` so activation stays concise.

### Offline-safe schema validation

Validation is provided by `scripts/validate.py` using bundled XSD files under `references/schemas/`.

The validator:

- auto-detects the document’s `rqml@version`
- supports `--schema-version` override
- uses a backend fallback chain: `xmllint → lxml → xmlschema`
- works offline for bundled schema versions
- supports JSON output for automation

### Semantic quality and traceability tooling

The repository also includes:

- `scripts/lint.py` — strictness-aware semantic linting
- `scripts/check_traces.py` — trace locator resolution
- `scripts/id_audit.py` — ID quality and change detection
- `scripts/extract.py` — requirement extraction as JSON
- `scripts/matrix.py` — Markdown traceability matrix generation

## Common use cases

Use this skill when you want a coding agent to help with tasks such as:

- creating or updating requirements in valid RQML format
- checking whether a spec is structurally valid
- enforcing acceptance-criteria and traceability expectations
- reviewing requirement coverage and verification links
- exporting requirement data for other tools
- generating review-friendly documentation from trace graphs

## Quick repository tour

- `SKILL.md` — agent activation entry point
- `references/activation.md` — activation and workflow cues
- `references/usage.md` — usage guidance
- `references/provenance.md` — schema provenance notes
- `references/schemas/` — bundled RQML XSDs
- `scripts/` — Python tooling
- `tests/` — regression coverage and fixtures
- `.rqml/adr/` — architecture decision records
- `.rqml/plan.md` — implementation plan
- `requirements.rqml` — this project’s own specification

## Requirements and runtime expectations

This repository is intentionally lightweight:

- Python **3.8+** is the baseline runtime for scripts
- no build or compilation step is required
- core validation is designed to work offline when a matching bundled schema is present
- optional backends such as `xmllint`, `lxml`, or `xmlschema` may affect which validation path is used

## If you are evaluating RQML for the first time

This skill is a good starting point if you want to see what an agent-friendly, traceability-focused requirements workflow looks like in practice.

The repository includes:

- a real RQML specification for the skill itself in `requirements.rqml`
- supporting ADRs under `.rqml/adr/`
- validation, linting, extraction, and matrix tooling
- test fixtures that show valid and invalid RQML documents

That makes it useful both as a tool and as a working example.

## About the wider RQML ecosystem

RQML has a broader home beyond this repository:

- **[rqml.org](https://rqml.org/)** is the canonical source for the RQML language, schemas, and core documentation
- **[rqml.dev](https://rqml.dev/)** is the tooling and developer-experience surface, including the VS Code extension and related tooling
- **this repository** provides the agent-workflow layer, helping coding agents participate more reliably in RQML-based software delivery

So the short version is:

- **rqml.org** defines RQML
- **rqml.dev** helps people use RQML in tools
- **rqml-skill** helps coding agents use RQML well

## Learn more

- [rqml.org](https://rqml.org/)
- [rqml.dev](https://rqml.dev/)
- [`SKILL.md`](./SKILL.md)
- [`references/`](./references/)
- [`scripts/`](./scripts/)
- [`requirements.rqml`](./requirements.rqml)

## Summary

The **RQML Agent Skill** is the fastest way to make coding agents more useful on RQML tasks.

It improves onboarding, reduces ambiguity, supports offline validation, and helps agents work with requirements and traceability as first-class engineering artifacts.
