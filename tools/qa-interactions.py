#!/usr/bin/env python3
"""交互回归（08-interactions.md / 05-typewriter.md）：复制按钮、平台切换、
双语切换、下拉 hover、卡片打字机、快速滚动安全网。对 ref/loc 各跑一遍做行为对齐。
用法: python3 tools/qa-interactions.py [shots_dir]"""
import sys, json, time
from playwright.sync_api import sync_playwright

CHROME = "/home/work/.cache/chrome-user/chrome-linux64/chrome"

def suite(page, base, tag, out):
    r = {}
    # 1. 复制按钮：is-copied 状态 + tooltip 淡入 + 1.5s 复位
    page.goto(base, wait_until="networkidle"); page.wait_for_timeout(500)
    page.click(".terminal__copy")
    r["copy_isCopied"] = page.eval_on_selector(".terminal__copy", "el => el.classList.contains('is-copied')")
    r["copy_tooltipOpacity"] = page.eval_on_selector(".terminal__copy-tooltip", "el => getComputedStyle(el).opacity")
    page.wait_for_timeout(1600)
    r["copy_autoReset"] = page.eval_on_selector(".terminal__copy", "el => !el.classList.contains('is-copied')")

    # 2. 平台切换：命令文本 + data-copy-text 同步 + is-active 迁移
    page.click('[data-platform="windows"]')
    r["win_cmd"] = page.eval_on_selector(".terminal__text", "el => el.textContent").strip()[:30]
    r["win_copyAttr"] = page.eval_on_selector(".terminal", "el => el.dataset.copyText")[:30]
    r["win_active"] = page.eval_on_selector('[data-platform="windows"]', "el => el.classList.contains('is-active')")
    page.click('[data-platform="unix"]')

    # 3. 双语切换：全量文本 + href 前缀 + 副标题直显译文（菜单需 hover 展开）
    page.hover(".hero__lang-trigger")
    page.wait_for_timeout(400)
    page.click('.hero__lang-option[data-lang="en"]')
    r["en_title"] = page.eval_on_selector("[data-i18n=featuresTitle]", "el => el.textContent.trim()")
    r["en_navHome"] = page.eval_on_selector("#navHome", "el => el.getAttribute('href')")
    r["en_subHasCaret"] = page.eval_on_selector(".hero__subtitle", "el => el.querySelector('.char') !== null")
    page.hover(".hero__lang-trigger")
    page.wait_for_timeout(400)
    page.click('.hero__lang-option[data-lang="zh"]')
    r["zh_title"] = page.eval_on_selector("[data-i18n=featuresTitle]", "el => el.textContent.trim()")
    r["zh_navHome"] = page.eval_on_selector("#navHome", "el => el.getAttribute('href')")
    r["zh_card1Chars"] = page.eval_on_selector(".card--1 h3", "el => el.querySelectorAll('.char').length")

    # 4. 产品下拉 hover：菜单淡入
    page.hover(".hero__nav-dropdown-trigger")
    page.wait_for_timeout(400)
    r["menu_opacity"] = page.eval_on_selector(".hero__nav-menu", "el => getComputedStyle(el).opacity")

    # 5. 卡片打字机：滚动入视口后字符逐步出现 → is-done
    page.goto(base, wait_until="networkidle"); page.wait_for_timeout(300)
    page.eval_on_selector(".card--1 h3", "el => el.scrollIntoView({block:'center'})")
    page.wait_for_timeout(250)
    r["type_t250ms"] = page.eval_on_selector(".card--1 h3", "el => el.querySelectorAll('.char.is-typed').length")
    page.wait_for_timeout(1800)
    r["type_done"] = page.eval_on_selector(".card--1 h3", "el => el.classList.contains('is-done')")
    r["type_total"] = page.eval_on_selector(".card--1 h3", "el => el.querySelectorAll('.char').length")

    # 6. 快速滚动安全网：瞬移滚到底 → 未播完的标题瞬显
    page.goto(base, wait_until="networkidle"); page.wait_for_timeout(300)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(150)
    r["snap_allShown"] = page.evaluate(
        "() => Array.from(document.querySelectorAll('.card__text h3')).every(h => h.querySelectorAll('.char.is-typed').length === h.querySelectorAll('.char').length)")

    page.screenshot(path=f"{out}/inter-{tag}.png")
    print(json.dumps({"tag": tag, **r}, ensure_ascii=False))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/work/.openclaw/workspace/.openclaw/tmp/shots"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True)
        for tag, base in [("ref", "https://mimo.xiaomi.com/coder"), ("loc", "http://localhost:8123/coder")]:
            ctx = b.new_context(viewport={"width": 1440, "height": 900})
            suite(ctx.new_page(), base, tag, out)
            ctx.close()
        b.close()
