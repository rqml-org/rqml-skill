# RQML Agent Skill

Bring **RQML** into any coding agent — Claude Code, Codex, OpenCode, Cursor, Gemini CLI, and every other host that supports the open [Agent Skills](https://agentskills.io) standard.

The **RQML Agent Skill** teaches agents the spec-first, five-stage RQML workflow and drives the **`rqml` CLI** ([`@rqml/cli`](https://www.npmjs.com/package/@rqml/cli)) for every operation — authoring, validation, lint, traceability, coverage, and the enforcement gate over `.rqml` requirements specifications. It ships **no engine of its own**: results are exactly what the canonical RQML toolchain produces, so the skill can never drift from it.

## Why this skill

- **Works on any skills host** — one open-standard `SKILL.md`, no per-host plugin required (the dedicated [rqml-claude](https://github.com/rqml-org/rqml-claude) and [rqml-codex](https://github.com/rqml-org/rqml-codex) plugins cover those two hosts; this skill covers everything else).
- **Always correct** — it delegates to `@rqml/cli`; there is no second engine to reimplement or keep in sync.
- **Spec-first** — it guides agents through the five-stage [Spec → Design → Plan → Code → Verify](https://rqml.org/docs/development-process) process rather than ad-hoc XML editing.
- **Low friction** — drop it in; the only dependency is `@rqml/cli` (or `npx @rqml/cli`), with no build step.

## Install

1. Copy this repository — or just its `SKILL.md` and `references/` — into a skills directory your host scans (for example `.claude/skills/`, `.agents/skills/`, or your host's equivalent).
2. Make the CLI available: `npm i -g @rqml/cli` (provides `rqml`), or rely on `npx @rqml/cli`. Requires **`@rqml/cli` ≥ 0.7.0**.
3. Activate it with a task involving `.rqml` files, requirements, validation, or traceability.

## What's inside

- `SKILL.md` — the activation entry point and command reference
- `references/usage.md` — the five-stage workflow, command by command
- `references/activation.md` — activation cues
- `requirements.rqml` — this skill's own RQML specification
- `.rqml/adr/` — its architecture decision records · `.rqml/plan.md` — its plan

## The wider RQML ecosystem

- **[rqml.org](https://rqml.org/)** — the RQML language, schema, and documentation
- **[rqml.dev](https://rqml.dev/)** — the tooling (the `rqml` CLI, the MCP server, the VS Code extension)
- **this repository** — the host-agnostic agent skill

Licensed under Apache-2.0.
