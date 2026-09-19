# kaomoji-dataset

**82,109 kaomoji** (Japanese text emoticons) with emotion, intent and subject labels in
**six languages** — English, Japanese, Chinese, Spanish, Portuguese and German.
No dependencies. 4.8 MB installed.

```bash
pip install kaomoji-dataset
```

```python
import kaomoji_dataset as kd

[k["text"] for k in kd.search("happy", limit=3)]
# → ['(◕‿◕)', '(・∀・)ノ', 'ヽ(ˇ∀ˇ )ゞ']

# the same three — the labels are cross-lingual
kd.search("嬉しい", limit=3)
kd.search("开心",  limit=3)
kd.search("feliz", limit=3)

kd.random(category="sad")["text"]   # → '(╥﹏╥)'
kd.stats["total"]                   # → 82109
```

Try it without writing any code:

```bash
kaomoji-dataset 嬉しい -n 5
kaomoji-dataset --categories
```

## Why this instead of the other kaomoji packages

Most kaomoji packages ship a few hundred entries hard-coded in one file, keyed by an English
word. This one is a **corpus**: 82,109 entries merged from 7 independent source families —
four open-source projects, 20 Japanese IME dictionaries, a web collection and our own earlier
library — deduplicated, and labelled so you can query it by *meaning* rather than by
remembering which English word the author happened to pick.

- **69,563 entries carry semantic labels** (85%) — emotion, intent, subject, drawn from a
  controlled vocabulary, not free text
- **Names and keywords in all six languages**, so the four queries above return the same rows
- **Tiered by shape**, so you can ask for just the clean faces: `core` (10,842) are pure
  faces with no dialogue; `mixed` and `verbose` carry Japanese text alongside
- **106 original kaomoji** designed for feelings that had none, marked `fontvibe-original`
- **Rendering flags** — `ascii_safe`, `needs_cjk_font`, `display_width` — so you know which
  ones survive a terminal, a tweet, or a font with no CJK coverage

## API

Every function returns plain `dict`s in the schema below — nothing to unwrap.

| | |
|---|---|
| `all()` | every entry as a list (`load()` is an alias, if you'd rather not shadow the builtin) |
| `search(q, lang=None, limit=50, tier=None)` | match names and keywords across all six languages; `limit=-1` returns every match |
| `by_category(name, limit=None, tier=None)` | one category |
| `by_emotion(label, limit=None, tier=None)` | one emotion label |
| `random(category=None, emotion=None, tier=None)` | one entry, or `None` |
| `categories()` | `[{"name": ..., "count": ...}]`, most populous first |
| `originals()` | the 106 marked `fontvibe-original` |
| `stats` | totals, tier breakdown, language list |

### Cost

The dataset ships gzipped and is parsed on first access, then cached. For the full 82,109,
measured on CPython 3.14 / Apple silicon: **~0.7 s** and **about 540 MB RSS**. That is not a
small amount of memory; budget for it before you import this inside a worker. Every call
after the first is free, so if you only need a handful of faces at import time, call
`random()` or `search()` once and keep the result.

Filtering does not avoid the parse — `by_category` still loads everything first. For a
one-off extraction from a memory-constrained job, stream the file yourself and keep only
what you need. Pulling the 10,842 `core` entries this way peaks at **83 MB** rather than 540:

```python
import gzip, json
from pathlib import Path
import kaomoji_dataset

path = Path(kaomoji_dataset.__file__).parent / "data" / "kaomoji.jsonl.gz"
with gzip.open(path, "rt", encoding="utf-8") as fh:
    core = [k for k in map(json.loads, fh) if k["tier"] == "core"]
```

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

Full field reference:
[SCHEMA.md](https://github.com/Funovate/fontvibe-kaomoji/blob/main/SCHEMA.md).
`id` is stable across releases.

## Other formats

This package carries the whole corpus as one gzipped JSONL. The GitHub repository also
publishes it split by tier as plain JSON, and as a flat CSV, along with the coverage
verification script:
[Funovate/fontvibe-kaomoji](https://github.com/Funovate/fontvibe-kaomoji).
There is a JavaScript package too: `npm i kaomoji-dataset`.

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
