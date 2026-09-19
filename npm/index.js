'use strict';
/*!
 * kaomoji-dataset — 82,109 kaomoji with six-language semantic labels.
 * Licensed CC BY 4.0 — attribution required. https://fontvibe.ai/tools/kaomoji
 */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const DATA = path.join(__dirname, 'data', 'kaomoji.jsonl.gz');
const LANGS = ['en', 'zh', 'ja', 'es', 'pt', 'de'];

let _all = null;

/** Parse the whole dataset once and cache it. ~0.6s, ~200 MB resident. */
function all() {
  if (_all) return _all;
  if (!fs.existsSync(DATA)) {
    throw new Error(
      'kaomoji-dataset: data file is missing (' + DATA + '). ' +
      'The package was probably published without running its prepack step; ' +
      'please open an issue at https://github.com/Funovate/fontvibe-kaomoji/issues'
    );
  }
  const raw = zlib.gunzipSync(fs.readFileSync(DATA)).toString('utf8');
  const out = [];
  for (const line of raw.split('\n')) {
    if (line) out.push(JSON.parse(line));
  }
  _all = out;
  return _all;
}

function norm(s) {
  return String(s == null ? '' : s).trim().toLowerCase();
}

/*
 * A negative limit used to fall through to slice(0, -n), which quietly returns
 * everything *except* the last n — a plausible-looking wrong answer. -1 is a
 * common "no limit" convention, so honour that instead.
 */
function take(arr, limit) {
  if (limit == null || limit < 0) return arr;
  return arr.slice(0, limit);
}

/**
 * Full-text search over names and keywords in all six languages.
 * @param {string} query
 * @param {{lang?: string, limit?: number, tier?: string}} [opts]
 */
function search(query, opts) {
  const o = opts || {};
  const q = norm(query);
  if (!q) return [];
  const langs = o.lang ? [o.lang] : LANGS;
  const hits = [];
  for (const k of all()) {
    if (o.tier && k.tier !== o.tier) continue;
    let score = 0;
    for (const lang of langs) {
      const name = norm(k.names && k.names[lang]);
      if (name === q) { score = 3; break; }
      if (name.includes(q)) { score = Math.max(score, 2); }
      const kws = (k.keywords && k.keywords[lang]) || [];
      for (const kw of kws) {
        const n = norm(kw);
        if (n === q) { score = Math.max(score, 3); }
        else if (n.includes(q)) { score = Math.max(score, 1); }
      }
    }
    if (score) hits.push({ score, k });
  }
  hits.sort((a, b) => b.score - a.score);
  return take(hits.map((h) => h.k), o.limit == null ? 50 : o.limit);
}

/** Every kaomoji in one category (see categories()). */
function byCategory(category, opts) {
  const c = norm(category);
  const o = opts || {};
  return take(all().filter((k) => norm(k.category) === c && (!o.tier || k.tier === o.tier)), o.limit);
}

/** Every kaomoji carrying one emotion label (English controlled vocabulary). */
function byEmotion(emotion, opts) {
  const e = norm(emotion);
  const o = opts || {};
  return take(
    all().filter((k) => (k.emotion || []).some((x) => norm(x) === e) && (!o.tier || k.tier === o.tier)),
    o.limit
  );
}

/** One random entry, optionally constrained. */
function random(opts) {
  const o = opts || {};
  let pool = all();
  if (o.category) { const c = norm(o.category); pool = pool.filter((k) => norm(k.category) === c); }
  if (o.emotion) { const e = norm(o.emotion); pool = pool.filter((k) => (k.emotion || []).some((x) => norm(x) === e)); }
  if (o.tier) pool = pool.filter((k) => k.tier === o.tier);
  if (!pool.length) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}

/** Sorted list of category names with their counts. */
function categories() {
  const m = new Map();
  for (const k of all()) m.set(k.category, (m.get(k.category) || 0) + 1);
  return [...m.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);
}

/** The 106 kaomoji designed by FontVibe, released under the same licence. */
function originals() {
  return all().filter((k) => k.origin === 'fontvibe-original');
}

const stats = require('./stats.json');

module.exports = { all, search, byCategory, byEmotion, random, categories, originals, stats, LANGS };
