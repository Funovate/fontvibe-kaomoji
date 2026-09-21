#!/usr/bin/env python3
"""Copy the dataset from the repo root into the package before building.

The .gz at the repo root is the single source of truth; it is never
committed twice.
"""
import shutil
import sys
import pathlib
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = root / "data" / "kaomoji.jsonl.gz"
dst = Path(__file__).resolve().parents[1] / "src" / "kaomoji_dataset" / "data" / "kaomoji.jsonl.gz"

if not src.exists():
    sys.exit(f"[sync-data] missing {src} — run this from inside the repo")

dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, dst)

size = dst.stat().st_size
if size < 1_000_000:
    sys.exit(f"[sync-data] copied file is only {size} bytes — refusing to build")
# stats.json 也必须跟着同步：它曾经是手工拷进来的副本，重建数据集后包里还是旧的
# （1.0.6 打包时 tagged 仍显示 69,563 而数据集已是 69,679）。⛔ 别再手工拷。
shutil.copyfile(root / "data" / "stats.json",
                pathlib.Path(__file__).resolve().parents[1] / "src" / "kaomoji_dataset" / "stats.json")

print(f"[sync-data] ok — {size / 1048576:.2f} MB + stats.json")
