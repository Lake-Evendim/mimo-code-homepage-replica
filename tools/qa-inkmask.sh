#!/bin/bash
# 动效验证：水墨擦除 canvas（04-ink-mask.md 验收）
# 定种子 RNG + 同步墨点爆发 → 三帧采样（早/中/晚）→ 露画像素面积趋势对比
# 用法: bash tools/qa-inkmask.sh <shots_dir> <ref|loc>
set -e
if [ ! -x "${AGENT_BROWSER_EXECUTABLE_PATH:-}" ]; then
  AGENT_BROWSER_EXECUTABLE_PATH="$HOME/.cache/chrome-user/chrome-linux64/chrome"
fi
export AGENT_BROWSER_EXECUTABLE_PATH
OUT="${1:?shots dir}"; TAG="${2:?ref|loc}"
BASE="https://mimo.xiaomi.com/coder"
[ "$TAG" = "loc" ] && BASE="http://localhost:8123/coder"

agent-browser set viewport 1440 900 >/dev/null
agent-browser open "$BASE" >/dev/null
agent-browser wait --load networkidle >/dev/null 2>&1 || true
sleep 2

# 定种子 + 沿对角轨迹同步派发 mousemove（stampAlong 自动补点），返回起点坐标
agent-browser eval '(function(){Math.random=function(){Math._s=(Math._s*1664525+1013904223)>>>0;return Math._s/4294967296};Math._s=42;var h=document.getElementById("hero");var r=h.getBoundingClientRect();h.dispatchEvent(new MouseEvent("mouseenter",{clientX:r.left+300,clientY:r.top+120}));for(var i=1;i<=24;i++){h.dispatchEvent(new MouseEvent("mousemove",{clientX:r.left+300+i*35,clientY:r.top+120+i*14}))}return "stamped"})()' >/dev/null

for t in 120 320 620; do
  agent-browser screenshot "$OUT/ink-${TAG}-t${t}.png" >/dev/null
  sleep 0.55   # 控制下一帧距爆发的间隔（命令往返 ~150ms）
done
agent-browser close >/dev/null 2>&1 || true
echo "ink frames -> $OUT/ink-${TAG}-t*.png"
