#!/bin/bash
# QA 采集脚本 —— 按 00-overall.md §4 验证方案产出基线/本地截图
# 三组对照：mimocode 壳页端到端（实测 zh，经301链）、/coder?lang=en、/coder?lang=zh
# 用法: bash tools/qa-capture.sh <shots_dir>
set -e
if [ ! -x "${AGENT_BROWSER_EXECUTABLE_PATH:-}" ]; then
  AGENT_BROWSER_EXECUTABLE_PATH="$HOME/.cache/chrome-user/chrome-linux64/chrome"
fi
export AGENT_BROWSER_EXECUTABLE_PATH
OUT="${1:?shots dir}"
mkdir -p "$OUT"

REF="https://mimo.xiaomi.com"
LOC="http://localhost:8123"

shot() { # $1=path — 截当前视口
  agent-browser screenshot "$OUT/$1" >/dev/null
}

settle_typewriters() { # 走完全页触发打字机安全网，再回顶
  agent-browser eval "window.scrollTo(0, document.body.scrollHeight)" >/dev/null
  sleep 2
  agent-browser eval "window.scrollTo(0,0)" >/dev/null
  sleep 1
}

capture_pair() { # $1=url $2=outprefix [--full]
  agent-browser open "$1" >/dev/null
  agent-browser wait --load networkidle >/dev/null 2>&1 || true
  sleep 3   # 副标题打字机收尾
  shot "${2}-hero.png"
  if [ "$3" = "--full" ]; then
    settle_typewriters
    agent-browser screenshot --full "$OUT/${2}-full.png" >/dev/null
  fi
}

agent-browser set viewport 1440 900 >/dev/null

# A. 壳页端到端（iframe 内页经301链落在 zh）
capture_pair "$REF/mimocode" "ref-mimocode"
capture_pair "$LOC/mimocode" "loc-mimocode"

# B/C. 内页双语（query 保留路由）
for lang in en zh; do
  capture_pair "$REF/coder?lang=$lang" "ref-$lang" --full
  capture_pair "$LOC/coder?lang=$lang" "loc-$lang" --full
done

agent-browser close >/dev/null 2>&1 || true
echo "captured -> $OUT"
