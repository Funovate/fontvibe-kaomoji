#!/usr/bin/env node
'use strict';
const k = require('./index.js');

const argv = process.argv.slice(2);
const flags = new Set();
const words = [];
let limit = 1;

for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '-n' || a === '--limit') {
    const v = parseInt(argv[++i], 10);
    if (!Number.isFinite(v) || v < 1) {
      console.error('--limit needs a positive number');
      process.exit(2);
    }
    limit = v;
  } else if (a.startsWith('-')) {
    flags.add(a);
  } else {
    words.push(a);
  }
}

if (flags.has('-h') || flags.has('--help')) {
  console.log(`kaomoji-dataset — ${k.stats.total.toLocaleString('en-US')} kaomoji, six languages

  npx kaomoji-dataset                 one random kaomoji
  npx kaomoji-dataset happy           search "happy" (en/zh/ja/es/pt/de all work)
  npx kaomoji-dataset 嬉しい -n 5      five results, Japanese query
  npx kaomoji-dataset --categories    list every category
  npx kaomoji-dataset --stats         dataset totals
  npx kaomoji-dataset --json happy    machine-readable output

Data CC BY 4.0 · https://fontvibe.ai/tools/kaomoji`);
  process.exit(0);
}

if (flags.has('--stats')) {
  console.log(JSON.stringify(k.stats, null, 2));
  process.exit(0);
}

if (flags.has('--categories')) {
  for (const c of k.categories()) console.log(String(c.count).padStart(7) + '  ' + c.name);
  process.exit(0);
}

const label = (r) => {
  const n = r.names || {};
  return n.en || n.ja || n.zh || r.category;
};

const q = words.join(' ');
let results;
if (q) {
  results = k.search(q, { limit });
} else {
  // 12.8% of the corpus carries no name in any language; a bare `npx kaomoji-dataset`
  // should still print something readable, so draw from the labelled part.
  const named = k.all().filter((r) => r.names && r.names.en);
  results = [];
  for (let i = 0; i < limit && named.length; i++) {
    results.push(named[Math.floor(Math.random() * named.length)]);
  }
}

if (flags.has('--json')) {
  console.log(JSON.stringify(results, null, 2));
  process.exit(0);
}

if (!results.length) {
  console.error('no match for "' + q + '"');
  process.exit(1);
}
for (const r of results) console.log(r.text + '  — ' + label(r));
