"""
Module to hold webserver-related code
"""

import os
import SimpleHTTPServer
import SocketServer
import threading
import settings

def start():
    """
    Start a thread to launch the webserver.
    """

    thread = threading.Thread(target = _start)
    thread.daemon = True
    print "Starting webserver thread serving at port", settings.WEB_LISTEN_PORT
    thread.start()

def _start():
    """
    Change working directory and start the webserver.
    """

    os.chdir(settings.WEBROOT_DIR)

    handler = RequestHandler
    httpd = SocketServer.TCPServer(("", settings.WEB_LISTEN_PORT), handler)
    httpd.serve_forever()

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data/traces.json":
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            trace_view.write(self.wfile)
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)