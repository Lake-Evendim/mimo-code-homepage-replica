#!/usr/bin/env python3
"""QA 数值 diff：均值差 / 差异像素占比 / 分区热力图。
用法: python3 tools/qa-diff.py <shots_dir> [pair ...]  默认比对四个标准对。"""
import sys, os
from PIL import Image, ImageChops

THRESH = 8  # 单通道差值阈值，低于视为同色

def diff(ref_p, loc_p, out_dir):
    a, b = Image.open(ref_p).convert("RGB"), Image.open(loc_p).convert("RGB")
    if a.size != b.size:
        return {"pair": os.path.basename(ref_p), "err": f"size {a.size} vs {b.size}"}
    d = ImageChops.difference(a, b)
    gray = d.convert("L")
    hist = gray.histogram()
    total = a.size[0] * a.size[1]
    over = sum(hist[THRESH:])
    mean = sum(i * n for i, n in enumerate(gray.histogram())) / total
    # 差异热力图（放大可视）
    heat = gray.point(lambda p: 255 if p > THRESH else 0)
    heat.save(os.path.join(out_dir, "diff-" + os.path.basename(ref_p)))
    return {"pair": os.path.basename(ref_p), "mean": round(mean, 3),
            "pct_over": round(100 * over / total, 3), "size": a.size}

if __name__ == "__main__":
    out = sys.argv[1]
    pairs = sys.argv[2:] or ["ref-mimocode-hero.png", "ref-en-hero.png", "ref-en-full.png", "ref-zh-hero.png", "ref-zh-full.png"]
    for p in pairs:
        ref = os.path.join(out, p)
        loc = os.path.join(out, p.replace("ref-", "loc-", 1))
        if not (os.path.exists(ref) and os.path.exists(loc)):
            print({"pair": p, "err": "missing file"}); continue
        print(diff(ref, loc, out))
