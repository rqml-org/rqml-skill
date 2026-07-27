#!/usr/bin/env node
// The minimum @rqml/cli version SKILL.md states is not this repository's to
// choose: it is the ecosystem floor, declared once in rqml-org/rqml and
// published at https://rqml.org/toolchain-floor.json (REQ-CLI-RUNTIME).
//
// The number has to appear literally in SKILL.md — a skill is prose an agent
// reads, often with no network — so the single-source rule cannot be enforced by
// removing it. It is enforced here instead: the vendored declaration must match
// the published one, and the number in the prose must match the vendored one.
// Without this check the two agree only until the floor first moves, which is
// exactly the divergence the ecosystem floor exists to end.
//
// Skips the network half when the canonical source is unreachable, so an offline
// run is not a spurious failure — the same rule the craft drift guards use.

import { readFileSync } from "node:fs";

const CANONICAL = "https://rqml.org/toolchain-floor.json";
const VENDORED = "toolchain-floor.json";
const SKILL = "SKILL.md";

let failed = false;

const vendoredText = readFileSync(VENDORED, "utf8");
const floor = JSON.parse(vendoredText).cliFloor;

if (typeof floor !== "string" || !/^\d+\.\d+\.\d+/.test(floor)) {
  console.error(`✗ ${VENDORED}: cliFloor "${floor}" is not a semantic version.`);
  process.exit(1);
}

// 1. The vendored copy tracks the published declaration.
let canonical = null;
try {
  const res = await fetch(CANONICAL, { signal: AbortSignal.timeout(10_000) });
  if (res.ok) canonical = await res.text();
} catch {
  canonical = null;
}

if (canonical === null) {
  console.warn(`• ${CANONICAL} unreachable; drift check skipped.`);
} else if (canonical !== vendoredText) {
  console.error(
    `✗ ${VENDORED} has drifted from ${CANONICAL}. Do not edit the vendored copy — ` +
      "change it in rqml-org/rqml (integrations/toolchain-floor.json) and re-vendor.",
  );
  failed = true;
} else {
  console.log(`✓ ${VENDORED} matches the published declaration.`);
}

// 2. The prose states that floor and no other.
const skill = readFileSync(SKILL, "utf8");
const stated = [...skill.matchAll(/@rqml\/cli`?\s*(?:≥|>=)\s*`?(\d+\.\d+\.\d+)/g)].map((m) => m[1]);

if (stated.length === 0) {
  console.error(`✗ ${SKILL} states no @rqml/cli minimum. REQ-CLI-RUNTIME requires one.`);
  failed = true;
} else {
  const wrong = [...new Set(stated)].filter((v) => v !== floor);
  if (wrong.length > 0) {
    console.error(
      `✗ ${SKILL} states @rqml/cli ≥ ${wrong.join(", ")}, but the ecosystem floor is ${floor}. ` +
        "Update the prose to the vendored value — never pick a minimum here.",
    );
    failed = true;
  } else {
    console.log(`✓ ${SKILL} states the ecosystem floor (${floor}).`);
  }
}

process.exit(failed ? 1 : 0);
