#!/usr/bin/env python3
"""Verify the coverage claim in README.md — independently, from upstream.

Fetches each upstream source live, parses out its kaomoji, and diffs against this
dataset. No trust in us required: everything it compares is downloaded at run time.

    python scripts/verify_coverage.py

Only stdlib. Comparison is byte-exact, same as how the dataset was deduplicated.
"""
import gzip, html, json, pathlib, re, sys, urllib.request

GH = "https://raw.githubusercontent.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "fontvibe-kaomoji-verify/1.0 (+https://github.com/Funovate/fontvibe-kaomoji)"}


def fetch(url, encoding=None):
    req = urllib.request.Request(url, headers=UA)
    raw = urllib.request.urlopen(req, timeout=60).read()
    if encoding:
        return raw.decode(encoding, "replace")
    for enc in ("utf-8", "utf-16", "cp932"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def rofimoji():
    t = fetch(f"{GH}/fdw/rofimoji/main/src/picker/data/kaomoji.csv")
    pat = re.compile(r"^(.*?)[ \t]+((?:[a-z][a-z\-]*)(?:,[ ]*[a-z][a-z\-]*)*)$")
    out = []
    for line in t.splitlines():
        if not line.strip():
            continue
        m = pat.match(line.rstrip())
        out.append((m.group(1).strip() if m else line.rstrip()))
    return [x for x in out if x]


def kaomoji_proj():
    t = fetch(f"{GH}/mtripg6666tdr/Kaomoji_proj/master/src/kaomoji.txt")
    out = []
    for line in t.splitlines():
        p = line.split("\t")
        if len(p) >= 2 and p[1].strip():
            out.append(p[1])
    return out


def emoji_nvim():
    j = json.loads(fetch(f"{GH}/Allaman/emoji.nvim/main/lua/data/kaomojis.json"))
    return [x for items in j.values() for x in items if isinstance(x, str)]


def rime():
    out = []
    t = fetch(f"{GH}/aoguai/rime_kaomoji_dict/master/data/lmeee_dict_data.txt")
    out += [html.unescape(m) for m in re.findall(r'data-clipboard-text="([^"]*)"', t)]
    t = fetch(f"{GH}/aoguai/rime_kaomoji_dict/master/data/sougou_dict_data.txt")
    out += [html.unescape(m) for m in re.findall(r'ywz_content">(.*?)</div>', t, re.S)]
    t = fetch(f"{GH}/aoguai/rime_kaomoji_dict/master/data/Temreg_dict_data.txt")
    out += [l.split("\t")[0].strip() for l in t.splitlines() if l.split("\t")[0].strip()]
    return out


SOURCES = [
    ("fdw/rofimoji", rofimoji),
    ("mtripg6666tdr/Kaomoji_proj", kaomoji_proj),
    ("Allaman/emoji.nvim", emoji_nvim),
    ("aoguai/rime_kaomoji_dict", rime),
]


# Upstream files carry entries in a rawer form than we store them: HTML entities left
# undecoded (`~(&gt;_&lt;~)`), and category labels from the scraped page glued onto the end
# (`(°))<< sea`, `┻━┻ミ＼（≧ロ≦＼） table`). Byte-exact comparison counts those as misses even
# though the kaomoji itself is covered — so report both: byte-exact, and after undoing
# exactly those two transformations. Nothing else is normalised; see SCHEMA.md "Identity".
TAIL = re.compile(r"\s+(?:sea|table|animal|cry|food|nature|people|objects?|symbols?)[,，]?\s*$")
# rime_kaomoji_dict glues a Chinese caption onto the front: `[噎住] ( *⊙~⊙)`
HEAD = re.compile(r"^\s*[\[【]([^\]】]{1,12})[\]】]\s*")


def norm(s):
    """Undo exactly the three things that differ between upstream form and ours.

    1. HTML entities, left undecoded upstream
    2. captions from the scraped page, glued onto the front (`[噎住] ( *⊙~⊙)`) or the end
    3. whitespace — when an entry only differed from one already present by spacing,
       the load kept one of them. So spacing is not an identity difference *for this
       comparison*; it still is inside the dataset (see SCHEMA.md "Identity").
    """
    s = html.unescape(s).strip()
    while True:
        t = HEAD.sub("", TAIL.sub("", s)).strip()
        if t == s:
            break
        s = t
    return "".join(ch for ch in s if not ch.isspace())


def load_ours():
    p = ROOT / "data" / "kaomoji.jsonl.gz"
    if not p.exists():
        sys.exit(f"missing {p} — run this from a checkout of the repo")
    with gzip.open(p, "rt", encoding="utf-8") as f:
        return {json.loads(line)["text"] for line in f}


def main():
    ours = load_ours()
    print(f"this dataset: {len(ours):,} unique kaomoji\n")
    ours_n = {norm(x) for x in ours}
    print(f"{'source':<32}{'entries':>9}{'exact':>9}{'':>10}{'normalised':>10}{'':>9}  {'missing':>7}")
    print("-" * 80)
    total_missing = 0
    missing_samples = []
    for name, fn in SOURCES:
        try:
            items = {x for x in fn() if x}
        except Exception as e:                       # network, layout change, rename…
            print(f"{name:<32}{'FETCH FAILED':>28}  {e}")
            continue
        covered = sum(1 for x in items if x in ours)
        miss_n = [x for x in items if norm(x) not in ours_n]
        total_missing += len(miss_n)
        print(f"{name:<32}{len(items):>9,}{covered:>9,}{covered/len(items)*100:>9.1f}%"
              f"{len(items)-len(miss_n):>10,}{(len(items)-len(miss_n))/len(items)*100:>9.1f}%  {len(miss_n):>7,}")
        missing_samples.extend(miss_n)
    print("-" * 80)
    if total_missing == 0:
        print("\n✅ every entry in every reachable source is present here.")
    else:
        print(f"\n{total_missing:,} upstream entries are not carried here.")
        print("These are entries we don't consider kaomoji — emoji, plain text, URLs, single")
        print("fragments, Japanese stage directions like (白目), and decorative rules (飾り罫).")
        print("README 'Why it isn't 100%' explains the policy. All of them:\n")
        for x in sorted(set(missing_samples), key=len):
            print(f"  {x[:70]}")
        print("\nDisagree about any of these? Open an issue — that feedback loop is how this")
        print("went from 93% to 99.9%.")
    print("\nNote: the Japanese IME dictionaries (the bulk of this dataset) are distributed as")
    print("LZH/ZIP archives from kaomoji.com and vector.co.jp and are not fetchable by a stdlib")
    print("script. They are listed in NOTICE; the counts in README come from the same merge run.")


if __name__ == "__main__":
    main()
