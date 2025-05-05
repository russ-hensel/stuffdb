#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 08:43:15 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------

import json
import socket
import subprocess
import sys
import time
import http.server
import threading
from urllib.parse import urlparse, parse_qs

class TabInfoHandler(http.server.BaseHTTPRequestHandler):
    """Handler for receiving requests from the Firefox extension"""

    # Store the response data at the class level
    response_data = None
    response_event = threading.Event()

    def do_POST(self):
        """Handle POST requests from the Firefox extension"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            request = json.loads(post_data.decode('utf-8'))
            print(f"Received request from extension: {request}")

            # Send response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
            self.end_headers()

            # Get active tab info and send response
            active_tabs = browser_tabs_query()
            if active_tabs:
                response = {
                    "title": active_tabs[0]["title"],
                    "url": active_tabs[0]["url"],
                    "success": True
                }
            else:
                response = {
                    "success": False,
                    "error": "No active tab found"
                }

            # Store the response data and signal that it's available
            TabInfoHandler.response_data = response
            TabInfoHandler.response_event.set()

            # Send the response back to the extension
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print(f"Sent response to extension: {response}")

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.end_headers()
            error_response = {"success": False, "error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Override to minimize console output"""
        if args and "200" not in args[0]:  # Only log non-200 responses
            print(format % args)


def browser_tabs_query():
    """Simulate the browser.tabs.query function for testing"""
    # In a real implementation, this would receive data from the extension
    # For now, we'll just return None to indicate we need the extension's response
    return None


def get_active_tab_info(timeout=10):
    """
    Get the title and URL of the active tab in Firefox.

    Args:
        timeout (int): Maximum time to wait for a response in seconds

    Returns:
        dict: A dictionary containing 'title' and 'url' of the active tab,
              or 'error' if something went wrong.
    """
    # Reset the response event and data
    TabInfoHandler.response_event.clear()
    TabInfoHandler.response_data = None

    # Setup HTTP server
    HOST = '127.0.0.1'
    PORT = 9999

    # Create and start server in a separate thread
    server = http.server.HTTPServer((HOST, PORT), TabInfoHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        print(f"Server started on {HOST}:{PORT}")

        # Trigger the extension using a custom URL scheme
        trigger_url = f"http://trigger-tabinfoprovider/?port={PORT}"

        if sys.platform == 'win32':
            subprocess.Popen(['start', 'firefox', trigger_url], shell=True)
        elif sys.platform == 'darwin':  # macOS
            subprocess.Popen(['open', '-a', 'Firefox', trigger_url])
        else:  # Linux
            subprocess.Popen(['firefox', trigger_url])

        print(f"Triggered Firefox with URL: {trigger_url}")

        # Wait for the response with timeout
        if TabInfoHandler.response_event.wait(timeout):
            return TabInfoHandler.response_data
        else:
            return {"error": "Timed out waiting for Firefox extension"}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        # Shutdown the server
        server.shutdown()
        server_thread.join(1)  # Join with timeout
        print("Server stopped")


# Example usage
if __name__ == "__main__":
    print("Getting active tab info...")
    tab_info = get_active_tab_info()
    print(json.dumps(tab_info, indent=2))




# ---- eof