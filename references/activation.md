# Activation Guide

Activate the RQML Agent Skill when a task involves `.rqml` files, requirements specifications, traceability, acceptance criteria, requirement coverage, or RQML validation.

## Activation cues

Activate when the prompt mentions:

- `rqml`
- `.rqml file`
- `requirements specification`
- `traceability`
- acceptance criteria · requirement coverage · schema validation · spec review

## What the skill does

It guides the five-stage, spec-first process (Spec → Design → Plan → Code → Verify) and drives the `rqml` CLI (`@rqml/cli`) for every operation. It ships **no engine of its own** — see `SKILL.md` for the CLI prerequisite (`@rqml/cli` ≥ 0.9.1) and the command reference.

## Repository layout

- `SKILL.md` — the activation entry point and command reference
- `references/authoring.md` — the canonical authoring craft: the six requirements-engineering activities, the markup each one lands in, and the findings that follow
- `references/monorepo.md` — which spec governs a file, and how discovery works
- `references/usage.md` — the five-stage workflow, command by command
- `references/activation.md` — this file
- `requirements.rqml` — this skill's own RQML specification
- `.rqml/adr/` — its architecture decision records · `.rqml/plan.md` — its plan
