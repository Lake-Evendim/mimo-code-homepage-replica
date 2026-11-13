#!/usr/bin/env python3
"""水墨擦除动效帧指标：hero 区露画像素数（非 #fcfaf8）+ 墨斑数。
用法: python3 tools/qa-ink-metrics.py <shots_dir>"""
import sys, os
from PIL import Image

BG = (252, 250, 248)  # 蒙版实色 --color-bg
HERO = (0, 0, 1440, 592)

def metrics(path):
    im = Image.open(path).convert("RGB").crop(HERO)
    px = im.load()
    w, h = im.size
    revealed = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if abs(r - BG[0]) + abs(g - BG[1]) + abs(b - BG[2]) > 24:
                revealed += 1
    return revealed * 4  # 折算全像素

if __name__ == "__main__":
    out = sys.argv[1]
    for f in sorted(os.listdir(out)):
        if f.startswith("ink-") and f.endswith(".png"):
            print(f"{f}: revealed≈{metrics(os.path.join(out, f))} px")
