# 08 · M8 交互 + 双语 i18n（SOURCE）

## 8a. 终端复制（IIFE #2）
- 点击 `.terminal__copy` → `copy()`：
  1. **先同步 `document.execCommand("copy")`**（textarea 兜底法）——源码注释：await Clipboard API 会消耗 user activation token，之后 execCommand 也会被拒。次序不能换。
  2. 再 fire-and-forget `navigator.clipboard.writeText`（现代 API 升级，catch 空）。
  3. 成功 → `.is-copied`（图标互换 + tooltip 上浮），1500ms 后自动移除（resetTimer 防抖）。
- 文本取 `.terminal[data-copy-text]`（平台切换会更新它）。

## 8b. 平台切换（IIFE #3）
- `commands = { unix: "curl -fsSL https://mimo.xiaomi.com/install | bash", windows: 'powershell -ep Bypass -c "irm https://mimo.xiaomi.com/install.ps1 | iex"' }`。
- 点击选项 → 改 `.terminal__text` 文本 + `data-copy-text` + 同步 `is-active`/`aria-pressed`。
- 无动画过渡（文本直接换）。

## 8c. 双语 i18n（IIFE #6）
- 字典 15 key：navDocs, navProduct, navMiMoDesktop, navBlog, navJoinUs, heroSubtitle, featuresTitle, card1Title..card5Body（10）, copyTooltip, copyAria。
- `applyLang(lang)` 做 7 件事：
  1. `document.documentElement.lang` = zh-CN / en；
  2. 语言菜单 `.is-active` 同步；
  3. `#docsBtn` href：`/zh/mimocode/start` ↔ `/mimocode/start`；
  4. `.terminal__copy` aria-label：复制命令 ↔ Copy command；
  5. `#blogBtn` href：`/zh/blog/mimo-code-long-horizon` ↔ `/blog/mimo-code-long-horizon`；
  6. 顶栏 href 前缀（zh 加 `/zh`，en 无）：navHome `prefix + "/"`、navMiMoCode `prefix + "/mimocode"`、navBlog `prefix + "/#blog"`、navJoinUs `prefix + "/#joinUs"`（源码注释：与主页 HomeNavLinks 一致）；
  7. `[data-i18n]` 文本替换：
     - `.hero__subtitle` 特例：清打字机状态、清锁宽、zh nowrap/en normal、直接显示译文；
     - `.card__text h3` 特例：重建 char spans + cursor，若已 typed 则新 span 直接 `is-typed`；
     - 其余元素直接 textContent。
- **初始语言**：`?lang=en` → en，否则 zh（iframe 壳固定传 lang=en，所以 /mimocode 路径下用户看到英文版）。
- 点击选项后 `opt.blur()`（收起 focus-within 下拉）。

## 还原要点
- `navMiMoCode` 菜单项文本 `MiMo Code` 不在字典里（品牌名），勿补。
- 语言切换是**同步直替换**，无过渡动画。
- `target="_top"` 的链接在 iframe 壳内跳出 iframe —— 保留原行为。
