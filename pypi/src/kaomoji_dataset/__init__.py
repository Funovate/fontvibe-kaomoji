"""82,109 kaomoji with emotion, intent and subject labels in six languages.

    >>> import kaomoji_dataset as kd
    >>> [k["text"] for k in kd.search("happy", limit=3)]
    ['(◕‿◕)', '(・∀・)ノ', 'ヽ(ˇ∀ˇ )ゞ']

Searching ``嬉しい``, ``开心`` or ``feliz`` returns the same three; the
labels are cross-lingual.

Data licensed CC BY 4.0 — attribution required.
https://fontvibe.ai/tools/kaomoji
"""

from __future__ import annotations

import gzip
import json
import random as _random
from pathlib import Path
from typing import Any, Dict, List, Optional

__version__ = "1.0.2"

LANGS = ("en", "zh", "ja", "es", "pt", "de")

_DATA = Path(__file__).parent / "data" / "kaomoji.jsonl.gz"
_STATS = Path(__file__).parent / "stats.json"

Kaomoji = Dict[str, Any]

_cache: Optional[List[Kaomoji]] = None


def all() -> List[Kaomoji]:  # noqa: A001 - mirrors the JavaScript package
    """Every entry, parsed once and cached (~0.9 s, ~250 MB resident)."""
    global _cache
    if _cache is not None:
        return _cache
    if not _DATA.exists():
        raise FileNotFoundError(
            f"kaomoji-dataset: data file is missing ({_DATA}). The package was "
            "probably built without running scripts/sync_data.py; please open an "
            "issue at https://github.com/Funovate/fontvibe-kaomoji/issues"
        )
    with gzip.open(_DATA, "rt", encoding="utf-8") as fh:
        _cache = [json.loads(line) for line in fh if line.strip()]
    return _cache


load = all  # for anyone who would rather not shadow the builtin


def _norm(value: Any) -> str:
    return ("" if value is None else str(value)).strip().lower()


def _take(items: List[Kaomoji], limit: Optional[int]) -> List[Kaomoji]:
    return items if limit is None else items[:limit]


def search(
    query: str,
    lang: Optional[str] = None,
    limit: Optional[int] = 50,
    tier: Optional[str] = None,
) -> List[Kaomoji]:
    """Match names and keywords across all six languages.

    An exact hit on a name or keyword outranks a substring hit.
    """
    q = _norm(query)
    if not q:
        return []
    langs = (lang,) if lang else LANGS
    hits = []
    for entry in all():
        if tier and entry.get("tier") != tier:
            continue
        score = 0
        for lg in langs:
            name = _norm((entry.get("names") or {}).get(lg))
            if name == q:
                score = 3
                break
            if q in name:
                score = max(score, 2)
            for kw in (entry.get("keywords") or {}).get(lg) or ():
                n = _norm(kw)
                if n == q:
                    score = max(score, 3)
                elif q in n:
                    score = max(score, 1)
        if score:
            hits.append((score, entry))
    hits.sort(key=lambda pair: pair[0], reverse=True)
    return _take([entry for _, entry in hits], limit)


def by_category(category: str, limit: Optional[int] = None, tier: Optional[str] = None) -> List[Kaomoji]:
    """Every entry in one category. See :func:`categories`."""
    c = _norm(category)
    return _take(
        [e for e in all() if _norm(e.get("category")) == c and (not tier or e.get("tier") == tier)],
        limit,
    )


def by_emotion(emotion: str, limit: Optional[int] = None, tier: Optional[str] = None) -> List[Kaomoji]:
    """Every entry carrying one emotion label (English controlled vocabulary)."""
    e = _norm(emotion)
    return _take(
        [
            k
            for k in all()
            if any(_norm(x) == e for x in k.get("emotion") or ())
            and (not tier or k.get("tier") == tier)
        ],
        limit,
    )


def random(
    category: Optional[str] = None,
    emotion: Optional[str] = None,
    tier: Optional[str] = None,
) -> Optional[Kaomoji]:
    """One random entry, or ``None`` when nothing matches the filter."""
    pool = all()
    if category:
        c = _norm(category)
        pool = [k for k in pool if _norm(k.get("category")) == c]
    if emotion:
        e = _norm(emotion)
        pool = [k for k in pool if any(_norm(x) == e for x in k.get("emotion") or ())]
    if tier:
        pool = [k for k in pool if k.get("tier") == tier]
    return _random.choice(pool) if pool else None


def categories() -> List[Dict[str, Any]]:
    """``[{"name": ..., "count": ...}]``, most populous first."""
    counts: Dict[str, int] = {}
    for k in all():
        name = k.get("category")
        counts[name] = counts.get(name, 0) + 1
    return [
        {"name": name, "count": count}
        for name, count in sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    ]


def originals() -> List[Kaomoji]:
    """The 106 kaomoji designed by FontVibe, marked ``fontvibe-original``."""
    return [k for k in all() if k.get("origin") == "fontvibe-original"]


def _load_stats() -> Dict[str, Any]:
    with _STATS.open(encoding="utf-8") as fh:
        return json.load(fh)


stats = _load_stats()

__all__ = [
    "all",
    "load",
    "search",
    "by_category",
    "by_emotion",
    "random",
    "categories",
    "originals",
    "stats",
    "LANGS",
    "Kaomoji",
    "__version__",
]
