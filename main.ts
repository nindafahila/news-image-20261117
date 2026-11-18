// news-image-20261117 — "The World in One Picture"
// A program/v1 entry for make.fun: it writes one image summing up the
// world news of Tuesday 17 November 2026 to /output/entry.png.
//
// The image itself is drawn by draw.py (pure Pillow, no network, fully
// deterministic) and stored in this repository as entry.png. This program
// only copies that image to the grader's output directory, so both graded
// runs write byte-identical output. Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target}`);
