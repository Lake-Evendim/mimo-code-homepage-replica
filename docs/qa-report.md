# QA 对比报告（BASELINE_VERIFY → PROJECT_VERIFY）

> 对比对象：线上 https://mimo.xiaomi.com/mimocode（壳）/ /coder（内页，经301链）
> 本地：site/（同构路径），服务 tools/serve.mjs（复刻线上301链）
> 方法：同视口 1440×900 截图数值 diff（PIL 通道阈值 8/255）+ 动效帧指标（露画像素面积/形态帧 diff）
> + 交互脚本回放（Python Playwright，ref/loc 同套对跑）。
> 采集/比对工具：tools/qa-capture.sh、tools/qa-diff.py、tools/qa-inkmask.py、tools/qa-ink-metrics.py、tools/qa-interactions.py

## 1. 静态截图对比
| 视图 | 线上基线 | 本地 | diff 均值 | 差异像素占比 | 结论 |
|------|----------|------|-----------|--------------|------|
| 壳页端到端 /mimocode | shots/ref-mimocode-hero.png | shots/loc-mimocode-hero.png | **0.0** | **0.00%** | **PASS** |
| hero 无鼠标（en） | shots/ref-en-hero.png | shots/loc-en-hero.png | **0.0** | **0.00%** | **PASS** |
| 全页（en，1425×3020） | shots/ref-en-full.png | shots/loc-en-full.png | **0.0** | **0.00%** | **PASS** |
| hero（zh） | shots/ref-zh-hero.png | shots/loc-zh-hero.png | **0.0** | **0.00%** | **PASS** |
| 全页（zh，1425×3028） | shots/ref-zh-full.png | shots/loc-zh-full.png | **0.0** | **0.00%** | **PASS** |

**五组全部像素级零差异（含字体渲染、字距、图像、留白）。**

## 2. 动效帧对比（水墨擦除 canvas，04-ink-mask.md）
验证环境注记：headless Chrome 默认 `hover:none` 会走触屏分支（canvas `display:none`），
故动效验证用 CDP `Emulation.setEmulatedMedia` 强制 `hover:hover` + 真实鼠标事件 + 定种子 PRNG。

| 检查项 | 预期 | 结果 | 结论 |
|--------|------|------|------|
| 静止 hero 蒙版全实色（无透画） | 每帧重涂 #fcfaf8 | 620ms 帧露画=0（蒙版完全愈合）ref/loc 均是 | PASS |
| 同轨迹爆发后 ~120ms 帧 | 洇边墨斑露画 | 露画面积 ref 146,908px / loc 157,784px（偏差 7.4%¹） | PASS |
| ~320ms 帧 | 墨斑愈合中 | ref 82,640px / loc 91,568px（偏差 10.8%¹），趋势一致 | PASS |
| ~620ms 帧 | 归零（LIFETIME 520ms） | 双双 0 | PASS |
| 洇边高频扰动形态（三频正弦毛边） | 形态一致 | 定种子中段帧逐像素 diff：**mean 0.15，>24 差异占比 0.00%** | PASS |
| 触屏分支 (hover:none) | canvas display:none，画直接可见 | 双方 display:none，背景区露画像素同为 9,552px（抽样区） | PASS |

¹ 面积偏差来自 rAF 相位/事件时序噪声（known-gaps #3），形态帧已证逐像素一致；验收按 04 的「形态+面积指标」执行。

## 3. 交互回归（ref/loc 同套对跑，结果一致）
| 交互 | 预期 | ref 实测 | loc 实测 | 结论 |
|------|------|----------|----------|------|
| 复制按钮 | tooltip 淡入结算 opacity=1，1.5s 后收起，is-copied 复位 | 1 → 0，复位 ✓ | 1 → 0，复位 ✓ | PASS |
| 平台切换 Windows | 命令换 powershell 版，data-copy-text 同步，is-active 迁移 | ✓ | ✓ | PASS |
| 语言切 English | featuresTitle/nav 全量英文化，navHome href=/，副标题直显译文（无 char 结构） | ✓ | ✓ | PASS |
| 语言切 简体中文 | 还原中文，navHome href=/zh/，卡片标题 char 结构重建（8 字符） | ✓ | ✓ | PASS |
| 产品下拉 hover | 菜单 opacity→1 淡入 | ✓ | ✓ | PASS |
| 卡片标题入视口 | 逐字打字，完成后 is-done | ✓（total=8, done） | ✓（total=8, done） | PASS |
| 快速滚动过卡 | 标题瞬显（安全网 snapShow） | ✓ | ✓ | PASS |

## 4. 复刻过程修正记录（QA 抓出的三个根因）
| # | 症状 | 根因 | 修复 |
|---|------|------|------|
| 1 | /mimocode 壳内实测为**中文**界面，与 ?lang=en 预期相反 | 线上301链 `/coder/index.html` → `/coder/index` → `/coder` **剥离 query**，?lang=en 是死参数（实测 wrapper iframe 落在 /coder，lang=zh-CN） | tools/serve.mjs 复刻同款301链；行为与线上一致 |
| 2 | 本地样式/脚本 rules:0、页面无样式（bodyH 9145） | 拆模块时 css/js 用**相对路径**，在无尾斜杠基路径 `/coder` 下解析到 `/css/...` 404 | 全部改绝对路径 `/coder/css|js/...`（与资产一致） |
| 3 | 壳页差 11%、内容偏移 (−8, 0) | 壳页 body 默认 margin 8px + 内联 iframe 基线间隙 → 外层出滚动条 → iframe 挤窄 15px → 居中布局偏移 | 壳页补 html/body margin:0 + overflow:hidden + iframe display:block（等价 Rspress 全局 reset） |

## 5. 结论
**PASS。** 五组静态对照全部 0.00% 差异；水墨擦除动效形态帧逐像素一致、面积趋势一致；
七项交互 ref/loc 行为完全一致。残余差异仅 known-gaps 表内条目，无新增、无需补偿调参。
