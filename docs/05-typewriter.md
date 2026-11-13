# 05 · M5 打字机动效 ×2（SOURCE）

## 5a. Hero 副标题（IIFE #5）
**触发**：`document.fonts.ready.then(type)`（无 fonts API 则直接 type）。
**守卫**：`matchMedia("(max-width: 700px)")` 命中 → 不打字（移动端可换行，锁宽会坏版）。
**算法**：
1. 临时 `white-space:nowrap` + 塞回原文，`getBoundingClientRect().width` 量整行宽；
2. `sub.style.width = ceil(w)px` **锁宽**（保证逐字打印时盒子不变、整体居中不抖）；
3. 清空文本，逐字包 `<span class="char">`，尾部加 `<span class="type-caret">`；
4. `START=350ms` 后逐字 `is-typed`（`DELAY=55ms`/字）；
5. 全部打完 +150ms 加 `is-done`（caret 动画停、opacity 0）。
**样式**：`.char{display:none}`→`.is-typed{display:inline}`；caret 2px×1.05em，`sub-caret` 0.75s step-end 闪烁。

## 5b. 卡片标题（IIFE #4）
**预处理**：所有 `.card__text h3` 逐字包 `.char` span（`white-space:pre`），尾部加 `<span class="cursor">`（2×18px 黑竖条，margin-left 3px）。
**触发**：IntersectionObserver，`threshold: 0.25`，进入视口 → `animateType`：
- 防重入 `dataset.typed="1"`，加 `is-active`（cursor 亮）；
- 逐字 `is-typed`，`CHAR_DELAY=130ms`/字；
- 完成后 `+120ms` 加 `is-done` → cursor 转 `cursor-blink`（1s steps(2,end) 无限闪烁，**不消失**）。
**安全网**：scroll（passive）时任何未打字标题 `getBoundingClientRect().bottom < innerHeight*0.5`（已被滚过中线）→ `snapShow` 瞬间全部显示 + is-active/is-done（防止快速滚动/锚点跳转后标题永远空白）。
**样式细节**：`.cursor` 默认 `opacity:0` + transition 180ms；`is-active` 才亮。

## 与 i18n 的耦合（见 08）
- 语言切换重建 h3 的 char spans：若 `dataset.typed==="1"` 则新 char 直接带 `is-typed`（保持已打完状态），重建 cursor；
- 副标题切换语言：移除 `is-typing/is-done`、清锁宽、直接显示译文（不重放打字机），nowrap 仅 zh。

## 还原要点
- 副标题 `.char{display:none}` 而卡片 h3 `.char{display:none}` + `.is-typed{display:inline-block}`（inline-block + pre）——两处实现略不同，勿统一。
- 打字机字符以 code point 迭代（`for..of`），中文/emoji 安全。
