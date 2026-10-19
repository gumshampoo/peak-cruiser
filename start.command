#!/bin/bash
# Double-click to start Peak Cruiser: runs the local server and opens the
# app in Chrome. Closing this window (or Ctrl+C) stops the server and puts
# the 3Dconnexion driver back if the app had paused it.
cd "$(dirname "$0")" || exit 1
python3 server.py &
SERVER=$!
trap 'kill -TERM $SERVER 2>/dev/null; wait $SERVER' EXIT INT TERM HUP
for _ in $(seq 1 30); do
  curl -s -o /dev/null http://127.0.0.1:8765/ && break
  sleep 0.1
done
open -a "Google Chrome" "http://localhost:8765/"
wait $SERVER
