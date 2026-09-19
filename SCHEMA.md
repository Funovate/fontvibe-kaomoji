# Schema

One record per kaomoji. Same shape in every data file.

```json
{
  "id": "kao_000042",
  "text": "ㅡ(￣ー￣)ㅡ✧",
  "category": "cool",
  "emotion": ["smug", "smirk", "proud", "gloating", "lenny", "triumph"],
  "intent":  ["give up", "defeat", "surrender", "done", "hopeless"],
  "subject": [],
  "names":    { "en": "Winning lying down", "zh": "躺赢", "ja": "寝たまま勝利", "…": "…" },
  "keywords": { "en": ["smug", "smirk", "…"], "zh": ["得意", "窃喜", "…"], "…": [] },
  "origin": "fontvibe-original",
  "locale_scope": ["*"],
  "tier": "core",
  "sources": ["fontvibe"],
  "ascii_safe": false,
  "needs_cjk_font": true,
  "display_width": 10,
  "length": 8
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | string | Stable across releases. Use it to reference an entry. |
| `text` | string | The kaomoji, **byte-exact**. Never normalised — see [Identity](#identity). |
| `category` | string | One of 52. Lowercased from the browsable site's category names. |
| `emotion` | string[] | What the face feels. English canonical terms. `[]` when unknown. |
| `intent` | string[] | What it's doing to you — greeting, apology, table flip… `[]` when unknown. |
| `subject` | string[] | What's in it — an animal, food, a weapon, sparkles… `[]` when unknown. |
| `names` | object | Short display name per locale. Keys: `en` `zh` `es` `pt` `de` `ja`. Absent when unlabelled. |
| `keywords` | object | Search terms per locale = `emotion` + `intent` + `subject` expanded into that language. |
| `origin` | string | `traditional` \| `fontvibe-original` |
| `locale_scope` | string[] | `["*"]` = shown to everyone on fontvibe.ai; `["ja"]` = shown only on the Japanese page (entries containing Japanese dialogue). Informational — **the data is yours to use however you like.** |
| `tier` | string | `core` \| `extended` \| `mixed` \| `verbose` — see [Tiers](#tiers). |
| `sources` | string[] | Which upstream families this entry was found in. |
| `ascii_safe` | bool | True if every character is ASCII. |
| `needs_cjk_font` | bool | True if it contains characters that need a CJK font to render correctly. |
| `display_width` | int | Terminal columns, counting East-Asian Wide/Fullwidth as 2. |
| `length` | int | Unicode code points. |

### Not included: `codepoints`

Deliberately omitted — it's one line, and shipping ~17 MB of derivable data would be padding:

```python
codepoints = [f"U+{ord(c):04X}" for c in rec["text"]]
```

---

## Tiers

Assigned by what fraction of an entry's characters appear in known pure-face samples.
The whitelist (950 characters) was derived empirically from 4,564 known dialogue-free
faces, not from Unicode character classes — because `ヒィ` / `チン` / `ｷｬﾊｯ` are used both
as facial features *and* as onomatopoeia, and no rule based on character class separates them.

| Tier | Count | Coverage | What it means |
|---|---:|---|---|
| `core` | 10,842 | 100% | Face only. Safe anywhere. |
| `extended` | 168 | ≥95% | Almost pure face. |
| `mixed` | 29,209 | ≥80% | Face plus a short Japanese phrase. |
| `verbose` | 41,890 | <80% | The 顔文字＋セリフ tradition — face plus a full line of Japanese dialogue. |

Building a picker for a non-Japanese audience? Use `core`.

---

## Identity

`text` is **byte-exact and never normalised**. This is deliberate, and it cost us a rewrite
to get right:

- NFKC normalisation merges `(⊙﹏⊙)` with `(⊙_⊙)` — wavy mouth vs. straight mouth.
  Different faces.
- It merges `ʕ　·ᴥ·ʔ` / `ʕ·ᴥ·　ʔ` / `ʕ·ᴥ·ʔ` — bear looking left, right, and straight ahead.
  Three different bears.
- Half-width and full-width katakana look the same to MySQL's default collation:
  `(^(エ)^)` and `(^(ｴ)^)` compare equal. They are two different kaomoji and both are here.

Within the collection pipeline, deduplication used byte-exact comparison only; whitespace-only
matches were flagged for human review, never merged automatically. When entries were loaded into
the published set, a whitespace-insensitive check did drop spacing variants of entries already
present — so a handful of upstream spacing variants resolve to one representative here.

If you need looser matching, normalise on your side — you can always go from exact to loose,
never the other way round.

---

## Labels

~90 concepts across three axes. Each concept expands into several search terms per language,
so `emotion: ["happy"]` becomes `["happy","smile","glad","cheerful","joy"]` in English and
`["开心","高兴","笑","喜悦","乐"]` in Chinese.

The expansions are written as **the words people in that market actually type**, not as
dictionary translations. Sometimes that means keeping English: the Chinese label for
`(っ-‸-c)` is `emo`, because that is what Chinese speakers type.

**12,546 entries (15%) carry no labels at all.** Where the source gave nothing to work with
and the glyphs weren't decisive, the field is empty rather than guessed. A confidently wrong
label is worse than a missing one.
