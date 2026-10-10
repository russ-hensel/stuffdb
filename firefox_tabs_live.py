#!/usr/bin/env python3
"""Get the current Firefox tab (and optionally tabs to its right), live.

Needs the Firefox Tabs Bridge extension installed and install.py run once.
No third-party libraries required.

As a library:
    from firefox_tabs_live import get_tabs, current_tab
    current_tab()          -> {"title": ..., "url": ..., ...}
    get_tabs(right=3)      -> [current, next, next, next]  (fewer if at the end)
    get_tabs(right=None)   -> current + every tab to its right

From the shell:
    python3 firefox_tabs_live.py          # current tab only
    python3 firefox_tabs_live.py 3        # current + 3 to the right
    python3 firefox_tabs_live.py --all    # current + all to the right
    python3 firefox_tabs_live.py 3 --json
"""
import argparse
import json
import os
import socket
import sys


class FirefoxTabsError(RuntimeError):
    pass


def socket_path():
    base = os.environ.get("XDG_RUNTIME_DIR") or "/tmp"
    return os.path.join(base, f"firefox_tabs_bridge-{os.getuid()}.sock")


def _query(request, timeout=6.0):
    path = socket_path()
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect(path)
            s.sendall((json.dumps(request) + "\n").encode("utf-8"))
            f = s.makefile("rb")
            line = f.readline()
    except (FileNotFoundError, ConnectionRefusedError):
        raise FirefoxTabsError(
            "Can't reach Firefox. Is Firefox running with the Tabs Bridge "
            "extension installed, and was install.py run?"
        ) from None
    except socket.timeout:
        raise FirefoxTabsError("Timed out talking to Firefox.") from None
    if not line:
        raise FirefoxTabsError("No response from the bridge host.")
    resp = json.loads(line)
    if not resp.get("ok"):
        raise FirefoxTabsError(resp.get("error", "unknown error"))
    return resp["result"]


def get_tabs(right=0):
    """Current tab followed by up to `right` tabs to its right (None = all)."""
    return _query({"cmd": "tabs", "right": right})


def current_tab():
    tabs = get_tabs(0)
    return tabs[0] if tabs else None


def main():
    ap = argparse.ArgumentParser(description="Show the current Firefox tab and tabs to its right.")
    ap.add_argument("right", nargs="?", type=int, default=0, help="how many tabs to the right (default 0)")
    ap.add_argument("--all", action="store_true", help="all tabs to the right")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    try:
        tabs = get_tabs(None if args.all else args.right)
    except FirefoxTabsError as e:
        sys.exit(f"error: {e}")

    if args.json:
        print(json.dumps(tabs, indent=2, ensure_ascii=False))
    else:
        for i, t in enumerate(tabs):
            label = "current" if i == 0 else f"+{i}"
            print(f"{label:>7}  {t['title'] or '(untitled)'}\n         {t['url']}")


if __name__ == "__main__":
    main()
