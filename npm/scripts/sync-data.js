#!/usr/bin/env node
// Copies the dataset from the repo root into the package before packing.
// The .gz is the single source of truth; it is never committed twice.
const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, '..', '..', 'data', 'kaomoji.jsonl.gz');
const dstDir = path.join(__dirname, '..', 'data');
const dst = path.join(dstDir, 'kaomoji.jsonl.gz');

if (!fs.existsSync(src)) {
  console.error('[sync-data] missing ' + src + ' — run this from inside the repo');
  process.exit(1);
}
fs.mkdirSync(dstDir, { recursive: true });
fs.copyFileSync(src, dst);

const bytes = fs.statSync(dst).size;
if (bytes < 1_000_000) {
  console.error('[sync-data] copied file is only ' + bytes + ' bytes — refusing to publish');
  process.exit(1);
}
// stats.json 也必须跟着同步：它曾经是手工拷进来的副本，重建数据集后包里还是旧的
// （1.0.6 打包时 tagged 仍显示 69,563 而数据集已是 69,679）。⛔ 别再手工拷。
const statsSrc = path.join(__dirname, '..', '..', 'data', 'stats.json');
fs.copyFileSync(statsSrc, path.join(__dirname, '..', 'stats.json'));

console.log('[sync-data] ok — ' + (bytes / 1048576).toFixed(2) + ' MB + stats.json');
