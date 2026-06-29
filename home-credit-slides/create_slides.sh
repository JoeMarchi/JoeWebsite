#!/usr/bin/env bash
# 使用 gws（Google Workspace CLI）將本簡報推送為 Google Slides。
#
# 前置：
#   1. 安裝 gws：npm install -g @googleworkspace/cli
#   2. 認證    ：gws auth login   （需瀏覽器 OAuth；本沙箱環境無法執行，請於本機跑）
#   3. 產生內容：python3 build_slides.py   （會輸出 batch_update.json / deck_title.txt）
#
# 註：gws 將 Discovery 的 path/query 參數對應到 --params、request body 對應到 --json。
#     若你的 gws 版本旗標不同，請以 `gws slides presentations --help`
#     及 `gws schema slides.presentations.batchUpdate` 確認後微調。
set -euo pipefail
cd "$(dirname "$0")"

command -v gws >/dev/null || { echo "找不到 gws，請先安裝並認證"; exit 1; }
[ -f batch_update.json ] || python3 build_slides.py

TITLE="$(cat deck_title.txt)"

echo "==> 建立簡報：$TITLE"
CREATE_OUT="$(gws slides presentations create --json "{\"title\": \"$TITLE\"}")"
echo "$CREATE_OUT"

# 解析 presentationId 與預設第一張投影片 objectId
PID="$(printf '%s' "$CREATE_OUT" | python3 -c 'import sys,json;print(json.load(sys.stdin)["presentationId"])')"
DEF_SLIDE="$(printf '%s' "$CREATE_OUT" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d["slides"][0]["objectId"])')"
echo "presentationId=$PID  預設投影片=$DEF_SLIDE"

# 將 batch_update.json 中的佔位符換成實際預設投影片 id
PAYLOAD="$(python3 -c 'import sys;print(sys.stdin.read().replace("__DEFAULT_SLIDE_ID__", sys.argv[1]))' "$DEF_SLIDE" < batch_update.json)"

echo "==> 寫入 13 張投影片內容"
printf '%s' "$PAYLOAD" | gws slides presentations batchUpdate \
  --params "{\"presentationId\": \"$PID\"}" \
  --json @- 2>/dev/null \
  || gws slides presentations batchUpdate \
       --params "{\"presentationId\": \"$PID\"}" \
       --json "$PAYLOAD"

echo "==> 完成！開啟： https://docs.google.com/presentation/d/$PID/edit"
