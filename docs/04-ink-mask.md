# 04 · M4 Hero 水墨擦除动效（Canvas2D）— web-shader-extractor 式报告

## TARGET_LOCK
- **渲染面**：`<canvas id="heroMask" class="hero__mask">`，Canvas2D context（非 WebGL/WebGPU；全站无 shader 管线）。
- **owner**：内联脚本 IIFE #1（源码 1383 行起）。
- **视觉行为**：canvas 整面涂 `#fcfaf8` 实色盖住 `.hero__bg` 的飞天画；鼠标滑过 hero 时沿轨迹"挖洞"露出画，洞（墨点）520ms 内扩张并愈合，形成毛笔洇墨式揭示。
- **证据等级**：`SOURCE`（算法源码完整可得）→ 直接按源码重建，不做视觉拟合、不补偿调参。

## 机制（渲染图）
```
每帧:
  source-over: fillRect 整面 rgb(252,250,248)     ← 重新盖住
  destination-out: 对每个存活墨点 carveInk()       ← 挖洞露出画
洞 = alpha 通道被挖穿 → 透出下层 .hero__bg 画
```
无存活墨点时停止 rAF（`running=false`），有新输入再启 —— 静止时零 GPU/CPU 占用。

## 参数表（全部 SOURCE）
| 参数 | 值 | 含义 |
|------|-----|------|
| MASK | `252,250,248` | 蒙版实色（= --color-bg） |
| R_START | 8 | 墨点出生半径 |
| R_END | 128 | 墨点目标半径基准 |
| R_VARY | 0.45 | 每点半径随机度（rmax = 128×(0.55~1.0)） |
| LIFETIME | 520ms | 墨点生命周期 |
| STAMP_STEP | 12 | 沿鼠标轨迹落点步距（插值补点） |
| MAX_STAMPS | 160 | 同时存活上限，超了 shift() 挤掉最老 |
| DPR | min(devicePixelRatio, 2) | 画布分辨率缩放上限 |

## 墨点形状 carveInk(x, y, r, alpha, seed)
- 径向渐变填充：内 0.25r 起 `rgba(0,0,0,.95α)` → 0.55 处 `.88α` → 边缘 0（软边）。
- 轮廓 32 段多边形，半径扰动 `wob = 0.78 + 0.14·sin(3a+seed) + 0.08·sin(7a+2.1seed) + 0.5·sin(13a+0.7seed)`（注：末项系数 0.05）—— 三频正弦模拟 feTurbulence 洇边。
- 每点独立 `seed = rand·2π`。

## 运动曲线
- 半径：`r = 8 + (rmax-8)·easeOutCubic(t)`，`ease = 1-(1-t)³`。
- 洞透明度：`alpha = 1 - t²`（先慢后快愈合）。
- t≥1 从 stamps 删除。

## 事件与生命周期
- `mouseenter`：落 origin 点（重置 lastX/Y）。
- `mousemove`：`stampAlong` 从上一点到当前点按 12px 插值补点。
- `mouseleave`：lastX/Y = null（下次进入不拉出长线）。
- `resize`：重算 canvas.width/height = w·DPR，并**显式设 style.width/height**（canvas 是替换元素，inset:0 不拉伸；否则光标与笔刷错位 DPR 倍 —— 源码注释点名的老 bug）。
- `ctx.setTransform(DPR,0,0,DPR,0,0)` 统一坐标系。
- 能力守卫：`matchMedia("(hover: hover)")` 不匹配（触屏）→ 直接 return；CSS 里 `@media(hover:none)` 双保险 `display:none`；移动端断点同样隐藏。

## REPLAY / BASELINE 计划
1. 本地页与线上页注入同一只鼠标轨迹脚本（dispatch MouseEvent 序列，同一路径同一节奏）。
2. 轨迹后固定延时截帧（~150ms / ~450ms 两个相位：扩张期/愈合期）。
3. 对比指标（数值，不依赖肉眼）：露出画像素占比（像素 ≠ #fcfaf8 的 hero 区域）、洞斑数量/分布、洇边高频纹理的存在性。
4. 容差：节奏性截帧存在 rAF 相位差，按"指标同量级 + 形态同类"验收，逐像素仅对静态区域强校验。
5. 静态基线（无鼠标）：hero 区域必须 100% 平色 —— 有画透出即 FAIL。
