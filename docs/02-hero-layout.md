# 02 · M2 Hero 布局层（SOURCE）

## 容器
`.hero`：`position:relative; height:592px; overflow:hidden; isolation:isolate`。

## z 分层（自下而上）
| 层 | 元素 | z-index |
|----|------|---------|
| 0 | `.hero__bg` 画 | 0 |
| 1 | `canvas#heroMask` 水墨蒙版 | 1 |
| 2 | `.hero__content` 文案区 | 2 |
| 3 | `.hero__logo-link` / `.hero__divider` | 3 |
| 4 | `.hero__bar` 顶栏 | 4 |

## 各元素几何（1440 设计稿）
- `.hero__bg`：absolute inset 0；`background-image:url(/coder/assets/飞天4.png?v=20260610-1851)`；`background-size:1440px 592px`；`background-position:bottom center`；no-repeat。
- `canvas.hero__mask`：absolute inset 0，`pointer-events:none`，display block（JS 内部处理 DPR）。
- `.hero__logo-link`：top 23px left 32px，141×18px，display block；`.hero__logo` img 100%×100%（HTML width=120 仅为固有属性）。
- `.hero__divider`：top 65px，高 1px，`#f3f0ef`，通栏。
- `.hero__bar`：absolute top 24px right 25px，height 15.32px，inline-flex，align center，gap 8px。

## 顶栏导航（`.hero__nav`，字体 "MiSans Medium"）
- 链接 `.hero__nav-link`：margin 0 6px，padding 8px 12px，15px/500，色 `#000`，nowrap；`::after` 底部 2.5px 黑下划线，`transform:scaleX(0)`→hover `scaleX(1)`，origin left，0.3s ease。
- 「产品」下拉：`.hero__nav-dropdown` relative；trigger = `.hero__nav-link` + caret svg（16px，`M16 22 6 12…` 三角）。
- `.hero__nav-menu`：absolute top 100% left 50% translateX(-50%) translateY(6px)→hover(2px)，min-width 160px，column，padding 12px 8px，白底，1px `rgba(0,0,0,.08)` 边，radius 12，shadow `0 12px 32px rgba(0,0,0,.12)`，opacity/visibility 过渡 0.3s，z-index 10。
- 菜单项 `.hero__nav-menu-item`：block，padding 8px 14px，radius 8，15px/400 黑，hover 底 `rgba(0,0,0,.06)`，transition 0.15s。
- 菜单内容：`MiMo Code`（#navMiMoCode→`/zh/mimocode`）、`MiMo 桌面版`（#navMiMoDesktop→`/go/desktop`）；之后 `博客`（#navBlog→`/zh/#blog`）、`加入我们`（#navJoinUs→`/zh/#joinUs`）。
- 所有导航链接 `target="_top"`（iframe 壳内点开要跳出 iframe —— 必须保留）。

## 语言切换器（`.hero__lang`）
- trigger：translate 图标 18×18（icon-translate.svg）+ caret，gap 5px；hover 下划线同 nav（`bottom:-2px`）。
- `.hero__lang-menu`：min-width 132px，`left:auto;right:0`，hover/focus-within translateY(6px)→(2px)。
- 选项按钮 `.hero__lang-option`：整宽左对齐透明按钮；`.is-active` 底 `rgba(0,0,0,.06)`；文本 `简体中文` / `English`。

## 还原要点
- 顶栏高度 15.32px 是内容自然高度，不要写死行高。
- 下拉的 hover/focus-within 双触发（键盘可达性）。
- nav 下拉项里 `navMiMoDesktop` 带 data-i18n，`MiMo Code` 无（品牌名不翻译）。
