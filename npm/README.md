# kaomoji-dataset

**82,109 kaomoji** (Japanese text emoticons) with emotion, intent and subject labels in
**six languages** — English, Japanese, Chinese, Spanish, Portuguese and German.
Zero dependencies. 4.8 MB installed.

```bash
npm i kaomoji-dataset
```

```js
const kaomoji = require('kaomoji-dataset');

kaomoji.search('happy', { limit: 3 });
// → (◕‿◕)   (・∀・)ノ   ヽ(ˇ∀ˇ )ゞ

// the same three — the labels are cross-lingual
kaomoji.search('嬉しい', { limit: 3 });
kaomoji.search('开心',   { limit: 3 });

kaomoji.random({ category: 'sad' }).text;  // → (╥﹏╥)
kaomoji.stats.total;                       // → 82109
```

ESM and TypeScript work out of the box:

```ts
import { search, byEmotion, stats, type Kaomoji } from 'kaomoji-dataset';
```

Try it without installing:

```bash
npx kaomoji-dataset 嬉しい -n 5
npx kaomoji-dataset --categories
```

## Why this instead of the other kaomoji packages

Most kaomoji packages ship a few hundred entries hard-coded in one file, keyed by an English
word. This one is a **corpus**: 82,109 entries merged from 7 independent source families —
four open-source projects, 20 Japanese IME dictionaries, a web collection and our own earlier
library — deduplicated, and labelled so you can query it by *meaning* rather than by
remembering which English word the author happened to pick.

- **69,563 entries carry semantic labels** (85%) — emotion, intent, subject, drawn from a
  controlled vocabulary, not free text
- **Names and keywords in all six languages** — searching `嬉しい`, `开心`, `feliz` and
  `happy` returns the same entries
- **Tiered by shape**, so you can ask for just the clean faces: `core` (10,842) are pure
  faces with no dialogue; `mixed` and `verbose` carry Japanese text alongside
- **106 original kaomoji** designed for feelings that had none, marked `fontvibe-original`
- **Rendering flags** — `ascii_safe`, `needs_cjk_font`, `display_width` — so you know which
  ones survive a terminal, a tweet, or a font that has no CJK coverage

## API

| | |
|---|---|
| `all()` | every entry as an array |
| `search(q, {lang, limit, tier})` | match names and keywords across all six languages; `limit` defaults to 50, `-1` returns every match |
| `byCategory(name, {limit, tier})` | one category |
| `byEmotion(label, {limit, tier})` | one emotion label |
| `random({category, emotion, tier})` | one entry, or `null` |
| `categories()` | `[{name, count}]`, most populous first |
| `originals()` | the 106 marked `fontvibe-original` |
| `stats` | totals, tier breakdown, language list |

### Cost

The dataset ships gzipped and is parsed on first access, then cached. For the full 82,109,
measured on Node 24 / Apple silicon: **~330 ms**, and it costs **212 MB of JS heap — about
610 MB RSS**. That is not a small amount of memory; budget for it before you `require` this
inside a serverless function. Every call after the first is free, so if you only need a
handful of faces at startup, call `random()` or `search()` once and hold on to the result.

## Entry shape

```json
{
  "id": "kao_000001",
  "text": "(◕‿◕)",
  "category": "happy",
  "emotion": ["happy", "smile", "glad", "cheerful", "joy"],
  "intent": [],
  "subject": [],
  "names": {
    "en": "Happy face", "ja": "にこにこ顔",   "zh": "开心脸",
    "es": "Cara feliz", "pt": "Cara feliz", "de": "Gesicht, fröhlich"
  },
  "keywords": {
    "en": ["happy", "smile", "glad"],
    "ja": ["嬉しい", "笑顔", "草", "www"],
    "zh": ["开心", "哈哈", "awsl"]
  },
  "origin": "traditional",
  "locale_scope": ["*"],
  "tier": "core",
  "sources": ["fontvibe"],
  "ascii_safe": false,
  "needs_cjk_font": false,
  "display_width": 5,
  "length": 5
}
```

The `keywords` above are abbreviated; the real record carries all six languages.

Full field reference: [SCHEMA.md](https://github.com/Funovate/fontvibe-kaomoji/blob/main/SCHEMA.md).
`id` is stable across releases.

## Other formats

This package carries the whole corpus as one gzipped JSONL. The GitHub repository also
publishes it split by tier as plain JSON, and as a flat CSV, along with the coverage
verification script:
[Funovate/fontvibe-kaomoji](https://github.com/Funovate/fontvibe-kaomoji).

## License — CC BY 4.0 (attribution required)

Free for commercial use, redistribution and modification. In exchange, **credit the source
where your users can see it**. The licence lets us specify the form; this is it:

```html
Kaomoji data from
<a href="https://fontvibe.ai/tools/kaomoji">FontVibe</a>
(CC BY 4.0)
```

Plain text, where a link is impossible:

```
Kaomoji data from FontVibe — https://fontvibe.ai/tools/kaomoji (CC BY 4.0)
```

A README line, an About page, a credits screen, or a source comment in the shipped file all
work. It only has to be somewhere a person can find it.

Full terms in [LICENSE](https://github.com/Funovate/fontvibe-kaomoji/blob/main/LICENSE);
upstream credits in [NOTICE](https://github.com/Funovate/fontvibe-kaomoji/blob/main/NOTICE).

The 106 original kaomoji and all the metadata we produced are additionally released as
**CC0** — public domain, no attribution needed for those.

---

Built and maintained by [FontVibe](https://fontvibe.ai).
Browse them rendered and one-click copyable at
[fontvibe.ai/tools/kaomoji](https://fontvibe.ai/tools/kaomoji) — the English page carries the
10,939 that render safely outside Japanese contexts, and
[顔文字一覧](https://fontvibe.ai/ja/tools/kaomoji) carries the whole corpus.
