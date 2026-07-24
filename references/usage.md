# Usage: the five-stage workflow

Every operation runs through the `rqml` CLI (`@rqml/cli` ≥ 0.9.1). Install with `npm i -g @rqml/cli`, or run on demand with `npx @rqml/cli`. The skill reimplements nothing — results are exactly the canonical engine's.

## Resolve the spec

`rqml` finds the governing spec by walking up from the working directory to the nearest `requirements.rqml` (or the sole `*.rqml`), stopping at the repository root. Pass an explicit path or `--base-dir <dir>` to override. In a monorepo, `rqml check --workspace` gates every discovered spec at once and returns one aggregated exit code.

## The stages and the activities inside them

The five stages are the workflow; the requirements-engineering activities are
what you are doing inside them (`references/authoring.md` has the full table).

| Stage | Activities it carries |
|-------|-----------------------|
| **Spec** | elicitation (what is wanted), analysis (what is in tension), specification (the obligation itself) |
| **Design** | analysis, recorded as ADRs and `<decision>` elements |
| **Plan** | none of its own — it sequences approved requirements |
| **Code** | implementation, plus management (keeping trace edges current) |
| **Verify** | verification (tests prove requirements), plus management (drift) |

Validation — a person agreeing these are the right requirements — runs across
the whole loop and is recorded by `rqml approve`.

## Spec — capture intent

- `rqml skeleton req` emits a schema-valid `<req>` to fill in (also `edge`, `testCase`, `stateMachine`). Never invent element shapes; `references/authoring.md` carries the shapes skeleton does not cover.
- Give each requirement one atomic, testable obligation and given/when/then `<acceptance>` criteria — tests are generated from these.
- Elicit before you specify: a requirement that `satisfies` no goal or scenario is an orphan, and the coverage report says so. Capture the goal or scenario it serves.
- `rqml validate` after every edit; never leave the spec invalid. This validates the **document** (schema + referential integrity) — it is not the stakeholder validation that `approved` records.
- Only `approved` requirements drive code. New requirements start as `draft`; the developer approves them with `rqml approve <ID>`.

## Design — record decisions

Write significant architectural decisions as ADRs in `.rqml/adr/` (`NNNN-slug.md`, flat and sequentially numbered). ADRs are immutable once accepted — supersede, don't edit. Mirror each as a `<decision>` in the spec.

## Plan — stage the work

Break the approved requirements into ordered stages in `.rqml/plan.md`.

## Code — implement with traces

- `rqml show <ID>` to read a requirement with its trace neighborhood; `rqml impact <ID>` before changing anything that exists.
- After implementing: `rqml link <ID> path/to/code.ts` records the `implements` edge and the drift baseline. Never hand-edit trace XML. `rqml link <from> <to> --type <type>` records any of the fifteen trace types, not just implements/verifiedBy.

## Verify — prove coverage

- `rqml link <ID> path/to/test --type verifiedBy` for each test.
- `rqml check` must exit 0 at the project's strictness — it combines document validation, trace coverage, and drift. `rqml lint`, `rqml status`, and `rqml matrix` surface quality and coverage detail.
- Report the finding, not the colour: name the requirement that has no verification edge, the goal no requirement satisfies, or the linked file that changed after its edge was recorded (a suspect link — re-read it, then update the requirement or re-pin with `rqml link --refresh <edge-id>`).

## Strictness

Pass `--strictness relaxed|standard|strict|certified` to `check` / `lint` to scale how aggressively the gate and lint report. There is no in-repo strictness config file; strictness is a CLI choice per invocation (or your host's policy).

Canonical reference: https://rqml.org/docs/tooling/cli
