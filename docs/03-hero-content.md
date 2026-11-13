# 03 · M3 Hero 内容层（SOURCE）

## 布局
`.hero__content`：relative z 2，`max-width:809px` 居中，`padding-top:180px`，column，align center，`gap:40px`。
`.hero__heading`：column，align center，gap 30px，text-align center，宽 100%。

## 标题/副标题
- `h1.hero__title`：margin 0，`--font-display`（Questrial），50px/400，letter-spacing .4px，色 ink。文本 `MiMo Code`。
- `p.hero__subtitle`：margin 0，`--font-mincho`（汇文明朝体），22px/**500**，ls .4px，line-height 1.5，nowrap，`max-width:min(940px,94vw)`。
- 打字机样式：`.char{display:none}` → `.char.is-typed{display:inline}`；`.type-caret` 2px×1.05em 竖线，margin-left 2px，vertical-align -0.18em，`sub-caret` 0.75s step-end 闪烁；`.is-done .type-caret` 动画停 + opacity 0（瞬间消失，无淡出过渡）。

## 安装区 `.install`（column，gap 16px）
### 平台切换 `.platform-switch`（role=group）
- inline-flex gap 4px padding 4px，底 `--color-chip-bg`，radius 46（胶囊）。
- 选项：padding 9px 22px，透明底无边，radius 46，MiSans 14px/500 ls .4px，色 `rgba(39,39,42,.45)`，hover 转 ink；`.is-active`：白底 + `0 1px 3px rgba(38,37,30,.12)` 阴影 + ink 字色；过渡 background-color/color/box-shadow 各 200ms ease。
- 两项：`Linux / macOS`（data-platform=unix，初始 active，aria-pressed=true）/ `Windows`（data-platform=windows）。

### 终端条 `.terminal`
- 600×55px（max-width 100%），padding 0 20px，底 `--color-chip-bg`，radius 10，MiSans 15px ls .4px，flex 两端对齐 gap 20px；`data-copy-text` 属性存命令全文。
- **联动动效**：`.hero:hover .terminal{background-color:#fff}`（280ms ease；`@media(hover:none)` 关闭）。
- `.terminal__prompt`：`>_`，色 `rgba(39,39,42,.45)`；`.terminal__cmd` 命令色 `#27272a`，溢出 ellipsis。
- 命令文本：unix `curl -fsSL https://mimo.xiaomi.com/install | bash`；windows `powershell -ep Bypass -c "irm https://mimo.xiaomi.com/install.ps1 | iex"`。
- 复制按钮 `.terminal__copy`：22×22，透明，hover opacity .7；focus-visible outline 2px ink offset 2。
  - copy 图标：icon-copy.svg 15×16.667，opacity .7；check 图标：svg 对勾 18×18 色 `#16a34a` opacity 0。
  - 互换动画：`.is-copied` 时 copy→opacity 0 scale .5；check→opacity 1 scale 1（200ms + 回弹曲线 `cubic-bezier(.34,1.56,.64,1)`）。
  - tooltip `.terminal__copy-tooltip`：绝对定位于按钮上方 10px，底 `#26251e` 字 `#fafafa` 11px/500 ls .2px radius 6 padding 5px 10px；初始 `translate(-50%,6px)` opacity 0 → `.is-copied` 时 `translate(-50%,0)` opacity 1（曲线 `cubic-bezier(.22,1,.36,1)` 280ms）；::after 4px 小箭头朝下。文本 zh `已复制` / en `Copied`（data-i18n=copyTooltip）。

## CTA `.ctas`（flex gap 20px）
`.btn`：inline-flex center，height 40px，min-width 130px，padding 10px 41px，radius 46，`"Microsoft Sans Serif", MiSans` 16px/500 ls .24px，透明底 + 1px `--color-border` 边，字色 ink；hover：底 ink 字 `#fafafa` 边 ink + `translateY(-1px)`（200ms）。
`.btn--primary`（Blog）：初始即 ink 底白字；hover 底/边转 `#3a3933`。
`.btn__arrow`（↗ 箭头 svg 16×16）：初始 `opacity:0; margin-left:-16px`（占位收紧）→ hover 或 primary 常态：`opacity:1; margin-left:10px`（200ms）。
三按钮：`GitHub`（外链 github.com/XiaomiMiMo/MiMo-Code，target _blank rel noreferrer noopener）、`文档`（#docsBtn→`/zh/mimocode/start`）、`Blog`（#blogBtn→`/zh/blog/mimo-code-long-horizon`）—— 均 `target="_top"` 或 _blank，注意保留。

## 还原要点
- primary 按钮箭头**默认显示**（不 hover 也显示），普通按钮 hover 才滑入。
- tooltip 是 `aria-hidden`，按钮 aria-label 动态改（复制命令/Copy command）。
- 副标题打字机逻辑见 05；max-width min(940px,94vw) 比 content 809px 宽——刻意让副标题可以超出容器。
