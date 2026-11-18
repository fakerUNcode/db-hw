#!/usr/bin/env bash
# ===================================================================
#  One-click launcher for macOS / Linux.
#  Usage:
#    bash start-mac-linux.sh [port]     (default port 8642)
#  Or make it double-clickable (macOS):
#    chmod +x start-mac-linux.sh && open start-mac-linux.sh
#  Stop the demo: press Ctrl+C.
# ===================================================================
cd "$(dirname "$0")" || exit 1

PORT="${1:-8642}"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "[ERROR] Python was not found on this machine."
  echo "  Option A: install Python 3 (https://www.python.org/downloads/)"
  echo "  Option B: skip the server - just open index.html in this"
  echo "            same folder with any browser. It runs fully offline."
  exit 1
fi

echo "=========================================================="
echo " Buffer Pool Page Replacement Demo (LRU vs LFU)"
echo "=========================================================="
echo "[1/2] Opening browser at http://127.0.0.1:${PORT}/index.html ..."
(
  sleep 1
  if command -v open >/dev/null 2>&1; then
    open "http://127.0.0.1:${PORT}/index.html"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://127.0.0.1:${PORT}/index.html"
  else
    echo "[hint] Open the URL above manually in your browser."
  fi
) &
echo "[2/2] Local server running. Press Ctrl+C to stop."
echo
exec "${PY}" -m http.server "${PORT}" --bind 127.0.0.1
