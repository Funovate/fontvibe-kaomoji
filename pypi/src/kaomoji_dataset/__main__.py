"""Command line entry point: ``kaomoji-dataset`` / ``python -m kaomoji_dataset``."""

from __future__ import annotations

import argparse
import json
import random as _random
import sys

from . import all as load_all
from . import categories, search, stats


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="kaomoji-dataset",
        description=f"{stats['total']:,} kaomoji, six languages.",
        epilog="Data CC BY 4.0 · https://fontvibe.ai/tools/kaomoji",
    )
    parser.add_argument("query", nargs="*", help="search in en/zh/ja/es/pt/de; omit for a random one")
    parser.add_argument("-n", "--limit", type=int, default=1, help="how many to print (default 1)")
    parser.add_argument("--categories", action="store_true", help="list every category")
    parser.add_argument("--stats", action="store_true", help="dataset totals")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if args.limit < 1:
        parser.error("--limit needs a positive number")

    if args.stats:
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return 0

    if args.categories:
        for c in categories():
            print(f"{c['count']:>7}  {c['name']}")
        return 0

    query = " ".join(args.query)
    if query:
        results = search(query, limit=args.limit)
    else:
        # 12.8% of the corpus carries no name in any language; a bare invocation
        # should still print something readable, so draw from the labelled part.
        named = [k for k in load_all() if (k.get("names") or {}).get("en")]
        results = [_random.choice(named) for _ in range(args.limit)] if named else []

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    if not results:
        print(f'no match for "{query}"', file=sys.stderr)
        return 1

    for r in results:
        names = r.get("names") or {}
        label = names.get("en") or names.get("ja") or names.get("zh") or r.get("category")
        print(f"{r['text']}  — {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
