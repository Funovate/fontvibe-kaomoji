# kaomoji

**82,109 kaomoji (Japanese text emoticons), with semantic labels in 6 languages.**

Browse and copy them all at **[fontvibe.ai/tools/kaomoji](https://fontvibe.ai/tools/kaomoji)**
— searchable, one click to copy, no install. This repo is the raw data behind it.

Every publicly available kaomoji dataset we could find is covered here at **97.8–100%**,
and the few entries that aren't are ones we deliberately exclude. You don't have to take
our word for any of it — [a script checks it against the live upstream files](#coverage).

```
82,109   kaomoji
69,563   with semantic labels (emotion / intent / subject) in en · ja · zh · es · pt · de
   106   original kaomoji, designed for feelings that had no kaomoji before
    52   categories
     4   tiers, split by how safely each renders outside Japanese contexts
```

---

## Coverage

Merged from 7 independent source families. Pairwise overlap between them is only 1–7% —
the kaomoji world is a set of near-disjoint islands, which is why no single existing
dataset is close to complete.

**Verify it yourself.** The script downloads each upstream file at run time and diffs it
against this dataset. Nothing is precomputed:

```bash
python scripts/verify_coverage.py     # stdlib only
```

Output as of the current release:

| Source | Entries | Covered | Not covered |
|---|---:|---:|---:|
| [fdw/rofimoji](https://github.com/fdw/rofimoji) — largest English-side set, 1.1k★ | 1,562 | **100.0%** | 0 |
| [Allaman/emoji.nvim](https://github.com/Allaman/emoji.nvim) | 2,016 | **99.9%** | 3 |
| [aoguai/rime_kaomoji_dict](https://github.com/aoguai/rime_kaomoji_dict) | 959 | **99.4%** | 6 |
| [mtripg6666tdr/Kaomoji_proj](https://github.com/mtripg6666tdr/Kaomoji_proj) (MIT) | 2,166 | **97.8%** | 48 |
| Japanese IME dictionaries (kaomoji.com + Vector, 20 files) | 77,086 | 100% | 0 |
| kaosute.net (web) | 449 | 100% | 0 |
| FontVibe's own earlier library | 1,525 | 100% | 0 |

> The bottom three are LZH/ZIP archives and a web page, not fetchable by a stdlib script;
> their numbers come from the same merge run and can be reproduced by re-running the
> collection pipeline. The four GitHub sources above are checked live, every run.
>
> `cspeterson/splatmoji` is byte-identical to rofimoji's data upstream, so it isn't listed separately.

### Why it isn't 100%

The 57 upstream entries not carried here are ones we don't consider kaomoji. The script
prints all of them so you can disagree:

| Excluded | Example |
|---|---|
| Emoji | `🥺` `🤯` `🍱` — a different thing; there are better emoji datasets |
| Plain text with no face | `RT` `OK` `カムサハムニダ` `呼ばれて飛び出てジャジャジャジャーン` |
| URLs | `https://twitter.com/settings/applications/` |
| Single characters and fragments | `` ` `` · `ﾟ` · `【:εω` |
| Japanese editorial annotations | `(白目)` `(困惑)` `(適当)` — stage directions, not faces |
| Decorative rules | `☆⌒Ｙ⌒Ｙ⌒Ｙ⌒Ｙ⌒☆` · `━─━─━─━─━` — 飾り罫, used *around* kaomoji |

Comparison is byte-exact, with three normalisations applied so that formatting differences
upstream don't read as gaps: HTML entities decoded, scraped captions stripped
(`[噎住] ( *⊙~⊙)`, `くコ:彡 sea`), and whitespace ignored. The script reports both the raw
byte-exact number and the normalised one.

**How the line is drawn:** by precedent, not by feel. Before excluding anything we check
whether this dataset already carries entries of the same kind. That check moved 18 entries
back in: bracketed single words like `(白目)` (17 precedents such as `（大爆笑）`), sparkle
clusters like `꙳★*ﾟ` (7 precedents), a face repeated in a row like `(p.-)(p.-)(p.-)`
(10 precedents), and everything 3 characters long — 242 such entries are already here and
all of them are real faces (`・ω・` `◕‿◕` `→_←`), so length alone was never a reason.

Think something in that list is a real kaomoji? **[Open an issue](https://github.com/Funovate/fontvibe-kaomoji/issues/new)** — three rounds of exactly
that feedback loop, run against ourselves, is how rofimoji went from 93.0% to 100.0%.

## What's different

Ranked by how strong the evidence is. We separate what we measured from what we're guessing.

### 1. 106 original kaomoji — the part that didn't exist before

Not collected — designed, for feelings that had no kaomoji yet: 躺平 (lying flat),
社死 (social death), doomscrolling, *saudade*, *Schadenfreude*, *mamihlapinatapai*.

Marked `"origin": "fontvibe-original"`. Checked for collisions three ways
(byte-exact / whitespace-insensitive / NFKC) against every collected entry: zero.

| | |
|---|---|
| `ㅡ(ᴗ_ᴗ)ㅡ` | lying flat — 躺平 |
| `(⊃///ω///⊂)` | social death — 社死 |
| `ㅡ(￣ー￣)ㅡ✧` | winning lying down — 躺赢 |
| `(・ω・)…(・ω・)ﾉ?` | mamihlapinatapai — two people each waiting for the other to act |

See [`data/originals.json`](data/originals.json).

### 2. Labels in six languages — measured

Every other public kaomoji dataset is **English-only**. rofimoji, the largest of them,
carries one English keyword per entry (often literally one word).

Here, 69,563 entries carry `emotion` / `intent` / `subject` in **en · ja · zh · es · pt · de**,
drawn from a controlled vocabulary of ~90 concepts, with the wording written to match
how people in each market actually type online rather than translated word-for-word.

This matters because kaomoji search demand is mostly not English:
Indonesia 15% · Mexico 11% · Brazil 10% · Chile 5% — over 40% non-English.

### 3. Semantic retrieval metadata — measured

Existing datasets give one keyword per entry, so searching `happy` recalls poorly.
Three labelled axes plus 52 categories make retrieval substantially better.

12,546 entries (15%) are deliberately left **unlabelled** rather than guessed at.
An honestly empty field beats a plausible wrong one.

### 4. Rendering metadata — **a hypothesis, not a finding**

`ascii_safe`, `needs_cjk_font`, `display_width` and the `tier` split are provided because
no other dataset has them. Whether developers actually *want* them, **we don't know** —
rofimoji has 1.1k stars with a single keyword per entry, which suggests existing needs are
being met reasonably well. If you have an opinion, [open an issue](https://github.com/Funovate/fontvibe-kaomoji/issues/new);
that's the fastest way for us to find out.

---

## Files

| File | Entries | Size | Use it for |
|---|---:|---:|---|
| `data/core.json` | 10,842 | 8.3 MB | **Start here.** Faces only, no Japanese dialogue — safest outside Japanese contexts |
| `data/extended.json` | 168 | 0.2 MB | Nearly pure faces |
| `data/mixed.json` | 29,209 | 25 MB | Face plus a short Japanese phrase |
| `data/verbose.json` | 41,890 | 35 MB | The Japanese 顔文字＋セリフ tradition — face plus a full line of dialogue |
| `data/kaomoji.jsonl.gz` | 82,109 | 4.7 MB | Everything, one JSON object per line |
| `data/kaomoji.csv` | 82,109 | 6.6 MB | `text,keywords` — drop-in shape for rofimoji-style pickers |
| `data/originals.json` | 106 | 0.1 MB | The original ones |
| `data/stats.json` | — | — | Counts, machine-readable |

Tiers are assigned by how much of an entry consists of characters that appear in
known pure-face samples. If you're building a picker for a non-Japanese audience,
`core.json` is the subset you want.

## Quick start

```python
import json, gzip
rows = [json.loads(l) for l in gzip.open("data/kaomoji.jsonl.gz", "rt", encoding="utf-8")]

happy_es = [r["text"] for r in rows if "feliz" in r["keywords"].get("es", [])]   # 27,856
safe     = [r for r in rows if r["tier"] == "core" and not r["needs_cjk_font"]]
```

```js
import rows from './data/core.json' with { type: 'json' }
const angry = rows.filter(r => r.keywords.ja?.includes('怒る'))   // 648 in core.json
```

Field definitions: [SCHEMA.md](SCHEMA.md).

---

## Attribution

CC BY 4.0 asks you to credit the source "in any reasonable manner requested by the licensor".
Here's what we ask for — copy whichever fits:

**Markdown**
```markdown
Kaomoji data from [FontVibe](https://fontvibe.ai/tools/kaomoji) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
```

**HTML**
```html
Kaomoji data from <a href="https://fontvibe.ai/tools/kaomoji">FontVibe</a> ·
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
```

**Plain text** (for a CLI, a NOTICE file, an app's about screen)
```
Kaomoji data from FontVibe — https://fontvibe.ai/tools/kaomoji — CC BY 4.0
```

A few things worth saying plainly:

- **Add `rel="nofollow"` if you prefer.** It's your page; we're not asking you to pass ranking
  signals, and we'd rather you credit us with a nofollow link than not credit us at all.
- **A link is not strictly required** — CC BY's exact words are "to the extent reasonably
  practicable". In a terminal app or a printed piece, plain text is fine.
- **Please link the site, not just this repo.** `fontvibe.ai/tools/kaomoji` is the canonical
  home: it's where all 82,109 are rendered, searchable and one-click copyable, and it's what
  your users will actually find useful. The repo is the raw data behind it.

## Citing it

There's a [`CITATION.cff`](CITATION.cff), so GitHub's "Cite this repository" button works.
BibTeX:

```bibtex
@misc{fontvibe_kaomoji,
  title        = {FontVibe Kaomoji Dataset},
  author       = {{FontVibe}},
  year         = {2026},
  version      = {1.0.0},
  howpublished = {\url{https://fontvibe.ai/tools/kaomoji}},
  note         = {82,109 kaomoji with semantic labels in six languages. CC BY 4.0}
}
```

## License

- **Data**: [CC BY 4.0](LICENSE). See [NOTICE](NOTICE) for upstream credits.
- **The 106 original kaomoji and all metadata we produced** (labels, names, tiers, rendering
  flags): **CC0** — public domain, no attribution needed at all.

CC BY rather than CC0 for the whole set because one upstream source is MIT-licensed and MIT
requires its copyright notice to be preserved, which CC0 cannot express.

Kaomoji themselves are a 25-year-old folk tradition with no identifiable authors.
Nothing here is claimed as ours except the 106 marked `fontvibe-original`.

## Contributing

Missing a source? [Open an issue](https://github.com/Funovate/fontvibe-kaomoji/issues/new) with a link — if it has entries we don't, we'll merge them
and update the coverage table. Found a mislabelled entry? PRs welcome; `id` is stable.

---

Built and maintained by [FontVibe](https://fontvibe.ai).
The browsable version, with all 82,109 rendered and searchable, is at
[fontvibe.ai/tools/kaomoji](https://fontvibe.ai/tools/kaomoji)
(Japanese: [顔文字一覧](https://fontvibe.ai/ja/tools/kaomoji)).
