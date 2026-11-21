// Entry program for the news-image-20261121 bounty (Node 22, stdlib only).
// The entry image is the entry.png beside this file, drawn from scratch by
// generate_image.py. This program copies it byte-for-byte into the grader's
// output directory, so both runs produce identical output. It reads nothing
// else, uses no network and no randomness.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

// An empty or whitespace-only MAKEFUN_OUTPUT_DIR counts as unset, so a
// stray empty variable cannot turn the output path into "".
const rawOut = process.env.MAKEFUN_OUTPUT_DIR?.trim();
const outDir = resolve(rawOut ? rawOut : "/output");

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);

// Fail loudly instead of silently shipping a truncated copy.
if (statSync(target).size !== statSync(source).size) {
  throw new Error(`entry.png copy incomplete: ${target}`);
}
