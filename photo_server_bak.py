#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:37:59 2026

@author: russ
"""

# ---- tof


# ---- imports


# photo_server.py  (or stick it in app startup)
import http.server, socketserver, threading
from   pathlib import Path

PHOTO_ROOT = Path("/mnt/8ball1/first6_root/photos/photos_db")  # whatever AppGlobal.parameters.picture_db_root is
PORT       = 8765

class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(PHOTO_ROOT), **kw)

def start_photo_server():
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print( "running as fast as i can ")
    return srv

start_photo_server()
print( "running?" )

# ---- eof ---------------------------


