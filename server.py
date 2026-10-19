#!/usr/bin/env python3
"""Local server for Peak Cruiser, with the SpaceMouse in direct mode.

Serves the app on http://localhost:8765 like `python3 -m http.server`.

While it runs, 3Dconnexion's driver (3DxWare 10) is paused so the page can
talk to the SpaceMouse directly over WebHID, which responds noticeably
faster than going through the driver. When the server stops -- Ctrl+C, the
Terminal window closed, or the process killed -- the driver is started
again, the same way it starts at login.

The driver is several cooperating apps (helper, navigation proxy, radial
menu, virtual numpad, 3Dconnexion Home), and they are always stopped and
started TOGETHER: restarting only the helper was tried first and left the
rest unable to reach the device, so the SpaceMouse stopped working in every
other app. While this server runs, other apps have no SpaceMouse; if one
still doesn't respond after the server stops, restart that app.

    GET /api/driver  -> {"mode": "direct" | "driver"}
"""
import json
import os
import signal
import subprocess
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8765
HELPER_PROCESS = "/Applications/3DconnexionHelper.app/Contents/MacOS/3DconnexionHelper"
HELPER_AGENT = f"gui/{os.getuid()}/com.3dconnexion.helper"
# Everything 3DxWare runs in the user session, quit politely first.
STACK_BUNDLE_IDS = [
    "com.3dconnexion.driver.helper",
    "com.3dconnexion.nlserver",
    "com.3dconnexion.RadialMenu",
    "com.3dconnexion.VirtualNumPad",
]
STACK_APP_NAMES = ["3Dconnexion Home"]
# ...and anything still left after that (the navigation proxy ignores quit).
STACK_PROCESS_PATTERNS = [
    HELPER_PROCESS,
    "/Applications/3Dconnexion/3DxNLServer/",
    "3DxRadialMenu.app/Contents/MacOS/",
    "3DxVirtualNumpad.app/Contents/MacOS/",
    "/Applications/3Dconnexion/3Dconnexion Home.app/",
]

stopped_by_us = False


def running(pattern):
    return subprocess.run(["pgrep", "-f", pattern], capture_output=True).returncode == 0


def stop_driver():
    global stopped_by_us
    if not running(HELPER_PROCESS):
        print("[driver] not running; nothing to pause", flush=True)
        return
    for bundle_id in STACK_BUNDLE_IDS:
        subprocess.run(["osascript", "-e", f'tell application id "{bundle_id}" to quit'],
                       capture_output=True, timeout=10)
    for name in STACK_APP_NAMES:
        subprocess.run(["osascript", "-e", f'quit app "{name}"'], capture_output=True, timeout=10)
    deadline = time.monotonic() + 4
    while time.monotonic() < deadline and any(running(p) for p in STACK_PROCESS_PATTERNS):
        time.sleep(0.2)
    for pattern in STACK_PROCESS_PATTERNS:
        if running(pattern):
            subprocess.run(["pkill", "-TERM", "-f", pattern], capture_output=True)
    stopped_by_us = True
    print("[driver] paused (SpaceMouse is direct to Peak Cruiser)", flush=True)


def start_driver():
    global stopped_by_us
    if not stopped_by_us:
        return
    stopped_by_us = False
    if not running(HELPER_PROCESS):
        # The helper's launch agent brings up the rest of the stack, as at login.
        subprocess.run(["launchctl", "kickstart", HELPER_AGENT], capture_output=True)
    print("[driver] resumed", flush=True)


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if self.path.startswith("/api/"):
            return
        super().log_message(fmt, *args)

    def do_GET(self):
        if self.path == "/api/driver":
            body = json.dumps({"mode": "direct" if stopped_by_us else "driver"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = ThreadingHTTPServer((HOST, PORT), Handler)

    def shutdown(*_):
        start_driver()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGHUP, shutdown)   # Terminal window closed
    stop_driver()
    print(f"Peak Cruiser: http://localhost:{PORT}  (Ctrl+C or close this window to stop)", flush=True)
    try:
        server.serve_forever()
    finally:
        start_driver()


if __name__ == "__main__":
    main()
