# 07 · M7 Footer（SOURCE）

- `.footer`：bg `#f5f4ef`，radius 0，min-height 290px，padding 40px 100px，flex 居中（align+justify center）。
- `.footer__inner`：flex wrap 居中，gap 6px，12px/400 ls 0.8px，色 `#504f49`，text-align center。
- 内容流：`Copyright©2025 Xiaomi. All Rights Reserved` │ `Cookie Policy` │ `Cookie Preferences`
  - 分隔符 `.footer__sep`：`|`，色 `#b1b1b1`，user-select none。
  - `.footer__link`：underline offset 3px thickness 0.5px，hover 色 ink（200ms）。
  - `.footer__btn`：裸按钮（无边框无底），font/letter-spacing inherit，hover 色 ink。
- 注意 `Copyright©2025` 中 © 两侧无空格（原样）。

## 还原要点
- min-height 290px 造成 footer 大面积留白 —— 这是原设计（画面下缘呼吸感），不要压缩。
- Cookie Policy href="#cookie-policy"、Cookie Preferences 为无行为按钮（原站也无绑定）。
