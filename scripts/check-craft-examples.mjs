#!/usr/bin/env node
// Extracts the markup examples from references/authoring.md, assembles them into
// one RQML document, and validates it with the rqml CLI (CRIT-CRAFT-EXAMPLES).
//
// Each example block in the reference is preceded by a marker naming the parent
// chain it belongs under:
//
//     <!-- rqml-example: domain/businessRules -->
//     ```xml
//     <rule id="…">…</rule>
//     ```
//
// The canonical craft is vendored by the plugins, so an invalid shape here would
// propagate to every host. This turns "the examples are valid" from a claim into
// a check.

import { readFileSync, mkdtempSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";

const SOURCE = "references/authoring.md";
// Top-level sections in the order the schema fixes; only these may be targeted.
const SECTION_ORDER = ["catalogs", "domain", "goals", "scenarios"];
// Sub-containers in the order each section's type declares them.
const SUB_ORDER = {
  catalogs: ["glossary", "actors", "stakeholders", "constraints", "policies", "decisions", "risks"],
  domain: ["overview", "entities", "businessRules"],
};

const markdown = readFileSync(SOURCE, "utf8");
const blocks = [...markdown.matchAll(/<!--\s*rqml-example:\s*([^\s>]+)\s*-->\s*\n```xml\n([\s\S]*?)\n```/g)];

if (blocks.length === 0) {
  console.error(`✗ ${SOURCE}: no <!-- rqml-example: … --> blocks found`);
  process.exit(1);
}

// section -> sub-container (or "") -> [snippet]
const tree = new Map();
for (const [, target, xml] of blocks) {
  const [section, sub = ""] = target.split("/");
  if (!SECTION_ORDER.includes(section)) {
    console.error(`✗ ${SOURCE}: example targets unknown section "${target}"`);
    process.exit(1);
  }
  if (sub && !(SUB_ORDER[section] ?? []).includes(sub)) {
    console.error(`✗ ${SOURCE}: example targets unknown container "${target}"`);
    process.exit(1);
  }
  if (!tree.has(section)) tree.set(section, new Map());
  const subs = tree.get(section);
  if (!subs.has(sub)) subs.set(sub, []);
  subs.get(sub).push(xml);
}

const indent = (xml, depth) =>
  xml.split("\n").map((l) => (l.trim() ? "  ".repeat(depth) + l : l)).join("\n");

const sections = [];
for (const section of SECTION_ORDER) {
  const subs = tree.get(section);
  if (!subs) continue;
  const body = [];
  const ordered = [...subs.keys()].sort(
    (a, b) => (SUB_ORDER[section] ?? []).indexOf(a) - (SUB_ORDER[section] ?? []).indexOf(b),
  );
  for (const sub of ordered) {
    const inner = subs.get(sub).map((x) => indent(x, sub ? 3 : 2)).join("\n");
    body.push(sub ? `    <${sub}>\n${inner}\n    </${sub}>` : inner);
  }
  // The scenario example names an actor; declare one so the document stands alone.
  if (section === "catalogs") body.push("    <actors>\n      <actor id=\"ACT-ANALYST\" name=\"Analyst\"/>\n    </actors>");
  sections.push(`  <${section}>\n${body.join("\n")}\n  </${section}>`);
}

const document = `<?xml version="1.0" encoding="UTF-8"?>
<rqml xmlns="https://rqml.org/schema/2.2.0" version="2.2.0" docId="CRAFT-EXAMPLES" status="draft">
  <meta>
    <title>Authoring-craft examples</title>
    <system>Generated from ${SOURCE}; validated in CI, never committed.</system>
  </meta>
${sections.join("\n")}
  <requirements>
    <req id="REQ-EXPORT-STREAM" type="FR" title="Large exports stream" status="draft" priority="must">
      <statement>The export service SHALL stream datasets larger than 10,000 rows.</statement>
      <acceptance>
        <criterion id="CRIT-EXPORT-STREAM">
          <given>A dataset of 10,001 rows</given>
          <when>An export is requested</when>
          <then>The response is streamed and peak memory stays below the buffer cap</then>
        </criterion>
      </acceptance>
    </req>
  </requirements>
</rqml>
`;

const dir = mkdtempSync(join(tmpdir(), "rqml-craft-examples-"));
const file = join(dir, "requirements.rqml");
writeFileSync(file, document);

try {
  execFileSync("npx", ["--yes", "@rqml/cli", "validate", file], { stdio: "pipe", encoding: "utf8" });
} catch (error) {
  console.error(`✗ ${SOURCE}: the markup examples do not assemble into a valid document\n`);
  console.error(error.stdout ?? "");
  console.error(error.stderr ?? "");
  console.error(`Generated document kept at: ${file}`);
  process.exit(1);
}

console.log(`✓ ${SOURCE}: ${blocks.length} markup examples assemble into a valid RQML 2.2.0 document`);
