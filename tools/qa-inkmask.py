#!/usr/bin/env python3
"""水墨擦除动效基线验证（04-ink-mask.md）：
CDP 强制 hover:hover（headless 默认 hover:none 会让脚本走触屏分支），
定种子 Math.random + 真实鼠标轨迹；页内真时钟采样露画像素（避开截图延迟噪声），
三帧趋势（扩张→愈合→归零）+ 一张中段帧留形态证据。
用法: python3 tools/qa-inkmask.py <shots_dir>"""
import sys, json
from playwright.sync_api import sync_playwright

CHROME = "/home/work/.cache/chrome-user/chrome-linux64/chrome"
SEED_JS = "Math.random=function(){Math._s=(Math._s*1664525+1013904223)>>>0;return Math._s/4294967296};Math._s=42;"

SAMPLER = """async () => {
  const c = document.getElementById('heroMask');
  const g = c.getContext('2d');
  const count = () => {
    const d = g.getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 3; i < d.length; i += 16) if (d[i] < 200) n++;
    return n * 4;
  };
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const out = [];
  for (const t of [120, 320, 620]) {
    await sleep(t === 120 ? 100 : 200);
    out.push([t, count()]);
  }
  return out;
}"""

def run(p, url, out, tag):
    b = p.chromium.launch(executable_path=CHROME, headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    ctx.add_init_script(SEED_JS)
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    cdp.send("Emulation.setEmulatedMedia", {"features": [
        {"name": "hover", "value": "hover"}, {"name": "any-hover", "value": "hover"},
        {"name": "pointer", "value": "fine"}, {"name": "any-pointer", "value": "fine"}]})
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(2000)
    hover = page.evaluate('matchMedia("(hover: hover)").matches')
    disp = page.evaluate('getComputedStyle(document.getElementById("heroMask")).display')
    # 同一轨迹：enter → 24 段对角线 mousemove（stampAlong 每 12px 自动补墨点）
    box = page.locator("#hero").bounding_box()
    x0, y0 = box["x"] + 300, box["y"] + 120
    page.mouse.move(x0, y0)
    page.mouse.move(x0 + 24 * 35, y0 + 24 * 14, steps=24)
    frames = page.evaluate(SAMPLER)  # 页内真时钟采样 [120,320,620]ms
    page.mouse.move(x0, y0)          # 再打一发，抓中段帧留形态证据
    page.mouse.move(x0 + 24 * 35, y0 + 24 * 14, steps=24)
    page.wait_for_timeout(150)
    page.screenshot(path=f"{out}/ink2-{tag}-morph.png")
    print(json.dumps({"tag": tag, "hover": hover, "canvas": disp,
                      "frames@120/320/620ms": frames}))
    b.close()

if __name__ == "__main__":
    out = sys.argv[1]
    with sync_playwright() as p:
        run(p, "https://mimo.xiaomi.com/coder", out, "ref")
        run(p, "http://localhost:8123/coder", out, "loc")
