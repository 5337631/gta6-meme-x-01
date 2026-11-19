// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is a post on X: a GTA 6 meme whose picture carries the
// make.fun ghost mascot and whose text carries the bounty link and our play
// code. This program's whole job is to hand that post's address to the
// grader: it reads POST.json at the repository root, sanity-checks its
// shape, and copies it byte for byte into the output directory.
//
// Local run (outside the grader, the env vars stand in for /bot and /output):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const POST_FILE = join(BOT_DIR, 'POST.json');

// Fail loudly on a malformed hand-in file instead of copying junk forward:
// the gate wants a small JSON object whose url is an X post address.
let parsed: unknown;
try {
  const raw = readFileSync(POST_FILE, 'utf8');
  if (Buffer.byteLength(raw, 'utf8') > 16384) {
    throw new Error('POST.json is larger than 16384 bytes');
  }
  parsed = JSON.parse(raw);
} catch (err) {
  console.error(`POST.json could not be read: ${(err as Error).message}`);
  process.exit(1);
}

const url = (parsed as { url?: unknown })?.url;
// Accept every address shape the house reads: /<handle>/status/<id> and
// /i/web/status/<id>, on x.com or twitter.com, with or without a query.
// A mismatch is only a warning: copying the file forward is this program's
// one job, and the gate -- not this program -- refuses a bad address.
const POST_URL_SHAPE =
  /^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/([^/]+\/status|i\/web\/status)\/\d+([?#].*)?$/;
if (typeof url !== 'string' || !POST_URL_SHAPE.test(url)) {
  console.error(`warning: POST.json url is not an X post address: ${String(url)}`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(POST_FILE, join(OUTPUT_DIR, 'POST.json'));
