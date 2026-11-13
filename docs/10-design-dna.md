# 10 · Design DNA（design-dna 三维度摘要）

> 依据 /design-dna skill 的 Phase-2 分析法，从 SOURCE 源码 + 截图提取。

## design_system（可度量）
- **color**：暖白纸感基调。bg `#fcfaf8`，ink `#26251e`，soft `#504f49`，border `#979696`，chip `#f3f0ef`；卡底 5 色低饱和暖灰（#efebe3/#f6f1ea/#efe8e3/#fbf2e9/#f5ede7）；accent 绿仅复制成功 `#16a34a`。整体近乎单色 + 飞天画点缀。
- **typography**：三主字体分工——Questrial（几何无衬线）只给两级展示标题；汇文明朝体（衬线）给副标题+卡片标题（文人画气质）；MiSans 给功能文本。中文展示 22px/500 lh1.447，正文 16px/300，功能 14-15px/500。等比约 50:30:22:16:12。
- **spacing**：hero 内容 padding-top 180、块间 40、组内 30/16；卡片列距 43；节奏宽松。
- **layout**：hero 居中单列 809px；features 1100px 五卡横向图文左右交替（杂志式）；footer 单行居中。
- **shape**：胶囊（radius 46）用于按钮/切换器；10-12px 圆角用于终端条/下拉菜单；卡片仅 4px。两种语言：交互=胶囊，容器=小圆角。
- **elevation**：极克制——仅下拉菜单一处阴影 `0 12px 32px rgba(0,0,0,.12)` + 平台选中态 `0 1px 3px`。
- **motion**：200-300ms ease/cubic-bezier(.22,1,.36,1) 微过渡；两处打字机（55ms/130ms 每字）；水墨擦除 520ms 生命周期回弹曲线。

## design_style（定性）
纸本画册 × 开发者工具：米白宣纸底 + 汇文明朝体 + 敦煌飞天画 = 东方文人画气质；叠加上终端命令条、GitHub CTA = 工程理性。克制留白、低饱和、无强色。品牌语气温润（"越用越懂你"）。原型 = editorial × minimal-tech，装饰度低，图像全部来自国画/工笔。

## visual_effects（超出 CSS 的表现）
| 效果 | 实现 | 强度 |
|------|------|------|
| 水墨擦除揭示（hero） | Canvas2D destination-out 荐划 + 三频正弦洇边 + 生命周期愈合 | ★★★（唯一重量级） |
| 副标题打印机 | DOM char span + 时序显隐 + 锁宽居中 | ★ |
| 卡片标题滚动打字 | IntersectionObserver + char span + 光标闪烁 | ★ |
| 按钮箭头滑入/反色、终端条 hero 联动变白、下拉菜单位移淡入 | 纯 CSS transition | ★ |
无 WebGL/3D/粒子/滚动视差。effect_intensity: 中低（一处重型+多处轻型）；performance_tier: 轻量（单 canvas + rAF 按需运行）。
