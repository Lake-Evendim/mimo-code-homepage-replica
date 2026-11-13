# 01 · M1 设计令牌 + 字体（SOURCE）

## 色彩令牌（:root）
| 变量 | 值 | 用途 |
|------|-----|------|
| --color-bg | `#fcfaf8` | 页面底色（暖白）；也是水墨蒙版实色 MASK=`rgb(252,250,248)` |
| --color-ink | `#26251e` | 主文字/主按钮底/下划线 |
| --color-ink-soft | `#504f49` | 卡片正文 |
| --color-border | `#979696` | 次按钮描边 |
| --color-chip-bg | `#f3f0ef` | 终端条/平台切换胶囊底 |

派生色（不走变量，散落各处）：`#fafafa`（按钮 hover 文字/tooltip 文字）、`#3a3933`（primary hover）、`#27272a`（终端命令/复制图标）、`rgba(39,39,42,.45)`（终端 prompt/未选中平台）、`#16a34a`（复制成功对勾）、`#f5f4ef`（footer 底）、`#b1b1b1`（footer 分隔符）、`rgba(0,0,0,.06/.08/.12)`（菜单 hover/描边/阴影）、卡片底色 5 色见 06。

## 字体令牌
| 变量 | 栈 | 实际生效 |
|------|-----|----------|
| --font-sans | PingFang SC, -apple-system, …, Microsoft YaHei | body 默认 |
| --font-mincho | "Huiwen Mincho", "Noto Serif SC", Songti SC… | 副标题、卡片标题（汇文明朝体） |
| --font-display | "Questrial", Century Gothic… | h1 "MiMo Code"、features 标题 |
| --font-misans | "MiSans", PingFang SC… | 终端/卡片正文/菜单/按钮 |
| --font-heiti | Heiti SC… | 定义未实际引用 |

@font-face（自托管子集）：
- `Huiwen Mincho` 400 → assets/huiwen-mincho-subset.woff2（仅覆盖用到的字形，缺字回退 Noto Serif SC 在线）
- `MiSans` 400 → assets/misans-subset.woff2
- `MiSans Medium` 500 → assets/misans-medium-nav-subset.woff2（仅顶栏）
外部：Google Fonts `Noto Serif SC 400,500` + `Questrial`（preconnect ×2 + css2 链接）。
按钮字体特殊：`.btn` 用 `"Microsoft Sans Serif", var(--font-misans)`。

## 基础样式
- `* { box-sizing: border-box }`
- html/body：margin/padding 0，bg `--color-bg`，color `--color-ink`，font-family `--font-sans`，-webkit-font-smoothing: antialiased，-moz-osx-font-smoothing: grayscale。

## 还原要点
- 三个 woff2 子集文件**原样搬运**（不重新子集化，避免字形覆盖漂移）。
- Google Fonts 链接原样保留。
- title 文本为 `MiMo Code`；html lang 初始 `zh-CN`（i18n 会改）。
