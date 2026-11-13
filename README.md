# mimo-code-homepage-replica —— MiMo Code 首页复刻

MiMo Code 首页的独立复刻项目，使用 HTML、CSS、JavaScript 和 Canvas 实现页面布局、水墨动效及双语交互。

仓库：https://github.com/Lake-Evendim/mimo-code-homepage-replica

本项目用于学习与页面还原，与 Xiaomi 官方项目无隶属关系。项目中保留的品牌、图片和字体等原站资产，其权利归原权利人所有。

目标：**复刻还原 https://mimo.xiaomi.com/mimocode 首页**（Xiaomi MiMo Code 落地页）。
方法：严格遵循 dulk-dev/my-shares《260628-用AI复刻一个复杂动效网站的思路》——
浏览器侦察+截图取证 → web-shader-extractor 式证据分析（动效部分）→ duck 式逐节点走查 →
按模块顺序执行、**每模块分析文档落盘** → 自运行 + 截图数值比对循环验证至一致。

## 验证结论（docs/qa-report.md）
- 静态：壳页端到端 + 双语 hero/全页 **五组对照全部像素级 0.00% 差异**
- 动效：水墨擦除 canvas 定种子形态帧 **逐像素一致（mean 0.15）**，露画面积趋势一致
- 交互：复制/平台切换/双语/下拉/打字机/快速滚动安全网 **七项与线上行为完全一致**

## 运行

需要 Node.js，无需安装 npm 依赖。在项目根目录执行：

```bash
node tools/serve.mjs 8123     # 零依赖；复刻线上301链（见 docs/known-gaps.md #6）
# 打开 http://localhost:8123/mimocode   ← 与线上同路径语义（壳页 iframe，实测中文界面）
# 内页直达 http://localhost:8123/coder[?lang=zh|en]
```
⚠️ 不要用纯静态服务器预览：线上 `/coder/index.html` 会301到 `/coder`（剥 query），
该路由行为是复刻的一部分，由 tools/serve.mjs 实现。

服务支持 Windows、macOS 和 Linux；URL 路由按正斜杠处理，以兼容 Windows。

## 目录
```
site/                     静态站（同构线上路径）
├── index.html            壳页（= /mimocode，iframe src=/coder/index.html?lang=en）
└── coder/
    ├── index.html        主页结构（hero / features / footer）
    ├── css/              tokens · base · hero · features · footer · responsive
    ├── js/               ink-mask · typewriter · interactions · i18n
    └── assets/           12 个原站资产（logo、飞天4.png、5 张特性画、2 图标、3 字体子集）
docs/                     分析文档（00~10 + qa-report + known-gaps，按模块落盘）
tools/                    serve.mjs（路由复刻）+ QA 工具（采集/数值diff/动效帧/交互回归）
```

## 文档索引
| 文档 | 内容 |
|------|------|
| docs/00-overall.md | 证据清单 + duck 式渲染主路径走查 + 模块执行顺序 |
| docs/01-design-tokens.md | 设计令牌（5 色 5 字体栈）+ 字体子集 |
| docs/02-hero-layout.md | Hero 分层（bg/蒙版/logo/divider/顶栏） |
| docs/03-hero-content.md | 标题/安装区/CTA |
| docs/04-ink-mask.md | **水墨擦除动效**（Canvas2D destination-out，参数表+验收计划） |
| docs/05-typewriter.md | 双打字机（副标题 55ms/字、卡片 130ms/字 + 安全网） |
| docs/06-features.md | 五卡布局（绝对定位图文左右交替） |
| docs/07-footer.md | 页脚 |
| docs/08-interactions.md | 复制/平台切换/i18n 行为表 |
| docs/09-responsive.md | ≤640px 断点 + hover:none 分支 |
| docs/10-design-dna.md | Design DNA 三维度（system/style/effects） |
| docs/qa-report.md | 对比验证报告（含修正记录） |
| docs/known-gaps.md | 诚实标注的残余差距 |

## QA 复跑
```bash
bash tools/qa-capture.sh /path/to/shots   # 采集（需本地 serve.mjs 已启动）
python3 tools/qa-diff.py /path/to/shots   # 数值 diff
python3 tools/qa-inkmask.py /path/to/shots # 动效帧（CDP 强制 hover:hover + 定种子）
python3 tools/qa-interactions.py          # 交互回归（ref/loc 同套对跑）
```
