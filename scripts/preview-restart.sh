#!/bin/sh
# Restart the local preview server (port 9292).
export PATH=$HOME/.local/node-v22.11.0-darwin-x64/bin:$PATH
cd "$(dirname "$0")/.."
pkill -f "node preview/server.mjs" 2>/dev/null
sleep 0.5
nohup node preview/server.mjs 9292 > "${PREVIEW_LOG:-/tmp/arvi-preview.log}" 2>&1 &
sleep 2
