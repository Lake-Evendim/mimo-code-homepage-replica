# 09 · M9 响应式（SOURCE）

## 断点 A：`@media (max-width: 640px)`
| 区 | 改动 |
|----|------|
| hero | height 425px，margin 0 |
| logo | top 33 left 20，109×14 |
| divider | top 66 |
| bar | top 29 right 19，gap 0；`.hero__nav{display:none}`（只留语言图标） |
| hero__bg | **top 67px bottom auto height 218px**（画变成横幅条） |
| hero__mask | display none |
| content | padding-top 129，gap 0，padding-x 20 |
| heading | gap 19 |
| title | 30px |
| subtitle | 14px，line-height 1.6，nowrap→normal |
| install | margin-top 54，gap 12，width 100% |
| platform 选项 | padding 6px 16px，12px |
| terminal | 100%（max 300），height 38，padding 0 14，10px |
| ctas | max 300，gap 13，margin-top 20 |
| btn | flex 1，height 33，min-width 0，padding 0 12，14px；arrow 12×12 |
| features | padding 30 0 50；title 22px margin 0 20 35；list 宽 auto margin 0 20 gap 30 |
| card×5 | height auto，padding 6px 6px 26px，flex column；painting `order:1` 转 static 100%×202；text `order:2` 转 static margin 26 20 0；h3 18px；p 14px |
| footer | min-height 217，padding 36；inner 9px ls .3 gap 5 |

## 断点 B：`@media (hover: none)`
- `.hero__mask{display:none}`（触屏无 hover 擦除语义）。

## JS 守卫（与 CSS 配套）
- ink-mask IIFE：`(hover: hover)` 不匹配即 return；
- 副标题打字机：`max-width: 700px` 即 return（比 CSS 断点 640 略宽 —— 原样保留）。

## 还原要点
- 卡片移动端 painting/text 的 position 全部转 static 并清 left/top —— 注意 5 张卡的独立选择器都要覆盖（源码用长选择器列表逐一清零）。
- 移动端卡片 DOM 顺序不改，靠 order 重排。
