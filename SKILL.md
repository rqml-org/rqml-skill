---
name: RQML Agent Skill
description: rqml, .rqml file, requirements specification, traceability — author, validate, lint, and trace RQML requirements documents through the five-stage spec-first process, driving the rqml CLI (@rqml/cli).
---

# RQML Agent Skill

Use this skill for any task involving `rqml`, an `.rqml file`, a `requirements specification`, `acceptance criteria`, or `traceability`.

RQML (https://rqml.org) is an XML format for software requirements. This skill guides you through the **five-stage, spec-first process** and drives the **`rqml` CLI** (`@rqml/cli`) for every operation. It adds no engine of its own, so its results are exactly what the canonical RQML toolchain produces.

## Prerequisite: the `rqml` CLI

Every operation runs through `@rqml/cli`. Check once, install if needed:

```bash
rqml --version          # already installed?
npm i -g @rqml/cli      # install the `rqml` command, or…
npx @rqml/cli <command> # …run on demand without installing
```

Requires **`@rqml/cli` ≥ 0.7.0** (for `lint`, `check --workspace`, and spec discovery). If neither `rqml` nor Node is available, tell the developer — never hand-author or "eyeball" validation.

## The five-stage process

RQML work follows **Spec → Design → Plan → Code → Verify** (https://rqml.org/docs/development-process). Each stage has a CLI move:

| Stage | Do | Commands |
|-------|----|----------|
| **Spec** | Capture intent as requirements with given/when/then acceptance criteria; only `approved` ones drive code | `rqml skeleton req`, `rqml validate`, `rqml approve <ID>` |
| **Design** | Record significant decisions as ADRs in `.rqml/adr/` (immutable; supersede, don't edit) | *(write the ADR)* |
| **Plan** | Break approved requirements into stages in `.rqml/plan.md` | *(write the plan)* |
| **Code** | Implement approved reqs; record trace links | `rqml show <ID>`, `rqml impact <ID>`, `rqml link <ID> <path>` |
| **Verify** | Prove coverage, catch drift; the gate must pass | `rqml link <ID> <test> --type verifiedBy`, `rqml check` |

## Command reference

```bash
rqml validate [path]    # XML well-formedness, XSD, referential integrity
rqml check [path]       # the gate: validation + coverage + drift (exit 0 = pass)
rqml lint [path]        # semantic lint; severity scales with --strictness
rqml status [path]      # coverage + lint summary
rqml show <ID>          # one artifact with its trace neighborhood
rqml impact <ID>        # what a change to <ID> affects, transitively
rqml overview [path]    # readable projection (--section / --id to scope)
rqml matrix [path]      # traceability matrix: status, goals, code, tests
rqml skeleton <kind>    # schema-valid snippet: req | edge | testCase | stateMachine
rqml link <ID> <uri>    # record an implements edge (+ --type verifiedBy for tests)
rqml approve <ID>       # transition a requirement's status (default approved)
rqml gate               # block implementing non-approved requirements
rqml check --workspace  # gate every spec in a monorepo, one aggregated exit code
```

`rqml` resolves the governing spec automatically by walking up from the working directory to the nearest `requirements.rqml` (or the sole `*.rqml`); pass a path or `--base-dir <dir>` to override. `--strictness relaxed|standard|strict|certified` scales how aggressively `check`/`lint` report.

## Non-negotiables

- **Validate after every edit** (`rqml validate`); never leave a spec invalid.
- **Finish with `rqml check`** — it must exit 0 at the project's strictness.
- **Never hand-edit trace edges** — use `rqml link` (it also records the drift baseline).
- **Never reimplement the engine** — every check goes through `rqml`.

## More detail

- `references/usage.md` — the five-stage workflow, command by command.
- `references/activation.md` — when to activate and the trigger cues.
- Canonical docs: https://rqml.org/docs/ · CLI reference: https://rqml.org/docs/tooling/cli
