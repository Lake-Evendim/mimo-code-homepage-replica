# 00 · 整体分析（duck 式结构走查）

> 方法来源：dulk-dev/my-shares《260628-用AI复刻一个复杂动效网站的思路》
> 流程：浏览器侦察+截图 → web-shader-extractor 式证据分析（动效部分）→ duck 式逐节点走查 → 按模块顺序执行、分析落盘 → 自运行+截图对比循环验证
> 目标站点：https://mimo.xiaomi.com/mimocode （MiMo Code 首页）

## 1. 侦察结果（证据清单）

证据等级标注：`SOURCE`（源码直接可得）/ `PARTIAL`（推断自截图/部分证据）/ `GUESS`（猜测）。

| # | 事实 | 证据 | 等级 |
|---|------|------|------|
| 1 | `/mimocode` 本身是 Rspress v1.46.2 SSR 壳页，body 内仅一个 100vh iframe 指向 `/coder/index.html?lang=en` | curl 抓取 wrapper HTML (9.5KB) | SOURCE |
| 2 | iframe 参数固定 `?lang=en`（Accept-Language 不影响，zh/en 两种请求头都返回 lang=en） | curl 对比验证 | SOURCE |
| 3 | 真正的首页 = `/coder/index.html`，55KB 单文件（内联 CSS + 内联 JS），title=`MiMo Code` | curl 抓取完整源码 (1887 行) | SOURCE |
| 4 | 页面语言默认 zh-CN，JS 根据 `?lang=en` 切英文 | 源码 i18n IIFE | SOURCE |
| 5 | 静态资产 12 个，全在 `/coder/assets/`：logo.png、icon-copy.svg、icon-translate.svg、飞天4.png(hero 背景画)、feature-{model,agent,context,evolution,compose}.png、huiwen-mincho-subset.woff2、misans-subset.woff2、misans-medium-nav-subset.woff2 | 源码引用扫描 + curl 全部下载成功 | SOURCE |
| 6 | 外部依赖仅 Google Fonts：Noto Serif SC(400,500) + Questrial | `<link>` in head | SOURCE |
| 7 | hero 有一个 Canvas2D「水墨擦除」动效（唯一 canvas/动效核心） | 源码内联脚本 + CSS 注释 | SOURCE |
| 8 | 无 WebGL/WebGPU/Three.js/视频资源 | 全源码扫描无相关 API | SOURCE |

**QUICK_SCOUT 结论**：该站动效层 = 1 个 Canvas2D 蒙版特效 + 2 处打字机 + 常规 CSS 过渡。
按 web-shader-extractor 的 SCOPE_CHECK：无 shader 管线，主证据走「源码直取」路线（SOURCE 优先于视觉拟合），
Canvas2D 部分照 capture-backends 的 Canvas2D 条款做截图证据采集 + 本地基线回放验证。

## 2. duck 式逐节点走查（渲染主路径）

对着完全不懂的人解释一遍页面从零到显示的完整数据流，每个节点回答：输入是什么 → 发生什么变换/副作用 → 输出什么：

```
浏览器请求 https://mimo.xiaomi.com/mimocode
  │ ✓ 输入: URL；输出: Rspress 壳 HTML
  ▼
壳页面 <iframe src="/coder/index.html?lang=en"> (100vw×100vh, border:none)
  │ ✓ iframe 加载内页；壳自身无其他可见内容（root 里只包着 iframe div）
  ▼
/coder/index.html 解析
  │ ✓ head: :root 设计令牌 (5 色 + 5 字体栈) → 3 个 @font-face 自托管子集字体
  │ ✓ Google Fonts CSS 注入 Noto Serif SC / Questrial
  │ ✓ 内联 <style> ≈1000 行：hero/features/footer + 2 处动效 CSS + 移动端断点
  ▼
<body> 渲染 3 个静态区块 + 5 个行为 IIFE
  │
  ├─ section.hero#hero (height 592px, overflow hidden, isolation:isolate)
  │    │ ✓ z-index 分层是关键：bg(0) → canvas 蒙版(1) → content(2) → logo/divider(3) → 顶栏(4)
  │    ├─ .hero__bg ── CSS background: url(飞天4.png), 1440×592, bottom center  【输入: 飞天画 PNG】
  │    ├─ canvas#heroMask ── 初始整面涂 #fcfaf8 实色，把画"盖住"                【动效 M4】
  │    ├─ .hero__logo-link ── logo.png (141×18, top 23 left 32)
  │    ├─ .hero__divider ── top 65px, 1px #f3f0ef
  │    ├─ .hero__bar ── 右上: 产品▾下拉 / 博客 / 加入我们 + 语言切换器▾
  │    └─ .hero__content ── 居中 max 809px, padding-top 180px
  │         ├─ h1.hero__title "MiMo Code" (Questrial 50px)
  │         ├─ p.hero__subtitle (汇文明朝体 22px) ── 打字机逐字浮现 【动效 M5a】
  │         ├─ .install ── 平台切换胶囊(Linux/macOS|Windows) + 终端命令条(复制按钮) 【交互 M8】
  │         └─ .ctas ── GitHub / 文档 / Blog 三个胶囊按钮(hover 反色+箭头滑入)
  │
  ├─ section.features
  │    ├─ h2.features__title "为什么选择 MiMo Code" (Questrial 30px)
  │    └─ .features__list (1100px) ── 5 张 card (360px 高, 43px 间距)
  │         │ ✓ 每卡 = 绝对定位的画(573×360 或 660×360) + 文本块(331px)，左右交替
  │         │ ✓ 卡底色各异: #efebe3/#f6f1ea/#efe8e3/#fbf2e9/#f5ede7
  │         └─ h3 标题 ── 滚动进入视口时逐字打字(130ms/字, IO threshold 0.25) 【动效 M5b】
  │
  ├─ footer.footer ── #f5f4ef 底, min-height 290px, 居中: Copyright | Cookie Policy | Cookie Preferences
  │
  └─ 6 个 IIFE 行为脚本（无框架，全部 vanilla JS）
       ① hero 水墨蒙版 (canvas destination-out 擦除)          → M4
       ② 终端复制按钮 (execCommand→clipboard, tooltip 1.5s)    → M8
       ③ 平台切换 (unix/windows 命令文本切换)                  → M8
       ④ 卡片标题打字机 (IO 触发 + scroll 安全网 snapShow)     → M5b
       ⑤ 副标题打字机 (fonts.ready 后开打, 55ms/字)            → M5a
       ⑥ i18n 双语切换 (data-i18n 字典 + href 前缀)            → M8
```

关键机制备忘（实现时最容易丢的细节）：
1. **canvas 是替换元素**：`inset:0` 不会拉伸它，必须 JS 显式设 `style.width/height`，否则光标和笔刷错位 DPR 倍。
2. **蒙版算法**：每帧先把整面重涂实色，再用 `globalCompositeOperation='destination-out'` 把活着的墨点挖掉（洞 = 透明 = 露出画）。墨点 520ms 生命周期：半径 8→rmax(easeOutCubic) 扩张，透明度 1-t² 洞愈合。
3. **墨点形状**：32 边形 + 三重正弦扰动 (sin3a/7a/13a) 模拟毛笔洇边；沿鼠标轨迹每 12px 落一点，上限 160 点。
4. **移动端 (hover:none)** canvas 直接 `display:none`，画全露 —— 触屏没有"擦"的动作。
5. **副标题打字机**会先量一次整行宽度锁宽，保证逐字打印时文字整体始终居中不抖。
6. i18n 切换会**重建**卡片标题的 char spans（保留已打字状态）并重置副标题。

## 3. 模块执行顺序（每模块产出 = 代码 + 本文档目录下分析 md）

| 顺序 | 模块 | 分析文档 | 实现目标 |
|------|------|----------|----------|
| M0 | 外壳 wrapper（iframe 壳页） | 00 (§1) | site/index.html |
| M1 | 设计令牌 + 字体加载 | 01-design-tokens.md | css/tokens.css |
| M2 | Hero 布局层（bg/logo/divider/顶栏） | 02-hero-layout.md | index.html 片段 + css |
| M3 | Hero 内容层（title/install/ctas） | 03-hero-content.md | 同上 |
| M4 | 水墨擦除动效（Canvas2D） | 04-ink-mask.md（shader-extractor 式报告） | js/ink-mask.js |
| M5 | 打字机动效 ×2 | 05-typewriter.md | js/typewriter.js |
| M6 | Features 五卡 | 06-features.md | index.html 片段 + css |
| M7 | Footer | 07-footer.md | 同上 |
| M8 | 交互+双语 i18n | 08-interactions.md | js/interactions.js |
| M9 | 响应式断点 | 09-responsive.md | css 内 media |
| — | Design DNA 总表 | 10-design-dna.md | — |
| — | QA 对比报告 / 已知差距 | qa-report.md / known-gaps.md | — |

## 4. 验证方案（BASELINE_VERIFY）

1. 本地起静态服务（python http.server），目录结构镜像线上：`/index.html`(壳) + `/coder/index.html` + `/coder/assets/`。
2. agent-browser 同视口 (1440×900) 对线上/本地各截：首屏、完整长图、features 滚动区、footer。
3. 逐模块比对截图 + `agent-browser diff`；动效用「录多帧对比」：脚本化鼠标路径擦出图案后截帧，对比露画面积/洇边形态。
4. 交互验证：复制按钮 tooltip、平台切换命令文本、语言切换全量文本、下拉菜单 hover。
5. 不一致 → 修复 → 重截，循环至达标；残余差异记录进 known-gaps.md（禁止补偿性调参掩盖证据缺失）。
