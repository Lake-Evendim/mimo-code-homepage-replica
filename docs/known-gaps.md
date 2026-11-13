# Known Gaps（诚实标注，禁止补偿调参掩盖）

> 标签：SOURCE（源码证据）/ PARTIAL（部分证据）/ GUESS（猜测）

| # | 差距/未知 | 等级 | 影响 | 处置 |
|---|-----------|------|------|------|
| 1 | 外壳页原为 Rspress v1.46.2 SSR（含字体加载 JS、search-container 等隐藏物）；复刻壳为等价极简 iframe 页 | PARTIAL | 视觉零差异（QA §1 壳页 0.00%），行为等价（target=_top 跳转路径保留） | 接受 |
| 2 | Google Fonts 在离线环境下不可达时 Questrial/Noto Serif SC 回退系统字体 | SOURCE（原站同样依赖） | 与原站行为一致，不算差异 | 接受 |
| 3 | 水墨擦除动效帧级像素对齐不可复现（rAF 相位、事件时序） | SOURCE | 逐帧像素 diff 不适用；定种子形态帧已证一致（mean 0.15），面积趋势验收（偏差 7–11%） | 按 04 计划验收，PASS |
| 4 | 字体子集仅覆盖 zh+en 两套词条的字形；若扩展词条需重新子集 | SOURCE | 与原站一致 | 接受 |
| 5 | Cookie Preferences 按钮线上无绑定行为 | SOURCE | 保留无行为 | 接受 |
| 6 | 线上路由 `/coder/index.html[?…]` →301→ `/coder/index` →301→ `/coder`（query 剥离）由服务端实现；纯静态托管无法复刻 | PARTIAL | 若不用 tools/serve.mjs 而用纯静态服务器，直达 /coder/index.html 时 ?lang= 仍生效，与线上301链行为不同 | 部署/预览一律走 tools/serve.mjs（README 已注明） |
| 7 | headless Chrome 默认 `hover:none`，水墨动效在无鼠标环境走触屏分支（线上同款行为） | SOURCE | 无头截图工具直接截图会拍到「画全露」形态（与真机鼠标环境不同，但与线上无头表现一致） | 动效验证已用 CDP 强制 hover:hover（tools/qa-inkmask.py） |
