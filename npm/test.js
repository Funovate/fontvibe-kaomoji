'use strict';
// Plain-node smoke test. No framework, no dev dependency.
const assert = require('assert');
const k = require('./index.js');

let n = 0;
const t = (name, fn) => { fn(); n++; console.log('  ok  ' + name); };

t('all() returns every entry', () => {
  assert.strictEqual(k.all().length, k.stats.total);
});

t('entries carry the documented shape', () => {
  for (const e of k.all().slice(0, 200)) {
    assert.ok(typeof e.id === 'string' && e.id);
    assert.ok(typeof e.text === 'string' && e.text);
    assert.ok(Array.isArray(e.emotion));
    assert.ok(e.names && typeof e.names.en === 'string');
    assert.ok(['core', 'extended', 'mixed', 'verbose'].includes(e.tier));
  }
});

t('ids are unique', () => {
  assert.strictEqual(new Set(k.all().map((e) => e.id)).size, k.stats.total);
});

t('search matches English', () => {
  assert.ok(k.search('happy', { limit: 5 }).length > 0);
});

t('search matches Japanese', () => {
  assert.ok(k.search('嬉しい', { limit: 5 }).length > 0);
});

t('search matches Chinese', () => {
  assert.ok(k.search('开心', { limit: 5 }).length > 0);
});

t('search honours limit', () => {
  assert.strictEqual(k.search('happy', { limit: 3 }).length, 3);
});

t('search defaults to 50 results', () => {
  assert.strictEqual(k.search('happy').length, 50);
});

t('a negative limit means no limit, not a truncated answer', () => {
  /* It used to fall through to slice(0, -1) and hand back everything but the
     last entry — a wrong answer that looks like a right one. */
  const every = k.search('happy', { limit: -1 });
  assert.ok(every.length > 50);
  assert.strictEqual(every.length, k.all().filter((e) =>
    k.LANGS.some((l) =>
      (e.names?.[l] || '').toLowerCase().includes('happy') ||
      ((e.keywords?.[l] || []).some((w) => String(w).toLowerCase().includes('happy'))))).length);
  assert.strictEqual(k.byCategory('happy', { limit: -1 }).length, k.byCategory('happy').length);
  assert.strictEqual(k.search('happy', { limit: 0 }).length, 0);
});

t('search of nonsense returns nothing', () => {
  assert.deepStrictEqual(k.search('zzzzqqqqxxxx'), []);
});

t('byCategory works', () => {
  const cats = k.categories();
  assert.ok(cats.length > 0);
  assert.ok(k.byCategory(cats[0].name).length === cats[0].count);
});

t('byEmotion works', () => {
  assert.ok(k.byEmotion('happy', { limit: 10 }).length > 0);
});

t('random respects its filter', () => {
  for (let i = 0; i < 50; i++) {
    assert.strictEqual(k.random({ tier: 'core' }).tier, 'core');
  }
});

t('originals() matches the published count', () => {
  assert.strictEqual(k.originals().length, k.stats.originals);
});

t('tier totals match stats', () => {
  const m = {};
  for (const e of k.all()) m[e.tier] = (m[e.tier] || 0) + 1;
  assert.deepStrictEqual(m, k.stats.tiers);
});

console.log('\n' + n + ' passed');
