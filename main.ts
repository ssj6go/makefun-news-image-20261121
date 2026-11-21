// Entry program for the news-image-20261121 bounty (Node 22, stdlib only).
// The entry image is the entry.png beside this file, drawn from scratch by
// generate_image.py. This program copies it byte-for-byte into the grader's
// output directory, so both runs produce identical output. It reads nothing
// else, uses no network and no randomness.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
