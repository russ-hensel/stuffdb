import http.server
import json
import socketserver
import threading
import time

class TabInfoRequestHandler(http.server.BaseHTTPRequestHandler):
    """Handler for the HTTP requests"""

    # Class variable to store the most recent tab info
    latest_tab_info = None
    tab_info_event = threading.Event()

    def do_POST(self):
        """Handle POST requests with tab information"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # Parse and store the received tab info
            tab_info = json.loads(post_data.decode('utf-8'))
            print(f"Received tab info: {tab_info}")

            # Update the class variables
            TabInfoRequestHandler.latest_tab_info = tab_info
            TabInfoRequestHandler.tab_info_event.set()

            # Send a response back to the extension
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"Tab info received")

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Override to control logging output"""
        if args and args[0].startswith("POST"):
            print(f"Request: {args[0]}")


def start_server(port=9999):
    """Start the HTTP server in a separate thread"""
    server = socketserver.TCPServer(("localhost", port), TabInfoRequestHandler)
    print(f"Server started on localhost:{port}")

    # Run the server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True  # Thread will close when the main program exits
    server_thread.start()

    return server, server_thread


def get_active_tab_info(timeout=5):
    """
    Get the title and URL of the active tab in Firefox.

    This function starts an HTTP server and waits for the Firefox extension
    to send the tab information.

    Args:
        timeout (int): Maximum time to wait for the tab info in seconds

    Returns:
        dict: A dictionary containing 'title' and 'url' of the active tab,
              or 'error' if something went wrong.
    """
    # Reset the event flag and latest tab info
    TabInfoRequestHandler.tab_info_event.clear()
    TabInfoRequestHandler.latest_tab_info = None

    # Start the server
    server, _ = start_server()

    try:
        print("Waiting for Firefox extension to send tab info...")
        print("Make sure to click the extension icon in Firefox or wait for the automatic poll")

        # Wait for the tab info with timeout
        if TabInfoRequestHandler.tab_info_event.wait(timeout):
            return TabInfoRequestHandler.latest_tab_info
        else:
            return {"error": f"Timed out waiting for tab info. Please make sure the Firefox extension is installed and click its icon."}

    except Exception as e:
        return {"error": f"Error: {str(e)}"}
    finally:
        # Shutdown the server
        server.shutdown()
        print("Server stopped")


# Example usage
if __name__ == "__main__":
    print("Getting active tab info...")
    print("Make sure the Firefox extension is installed.")

    tab_info = get_active_tab_info()
    print("\nResult:")
    print(json.dumps(tab_info, indent=2))

#     from tab_info import get_active_tab_info

# # Get the active tab information
# tab_info = get_active_tab_info()

# # Use the information
# if "error" not in tab_info:
#     print(f"Current tab: {tab_info['title']}")
#     print(f"URL: {tab_info['url']}")
# else:
#     print(f"Error: {tab_info['error']}")