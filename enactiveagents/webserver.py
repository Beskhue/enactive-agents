"""
Module to hold webserver-related code
"""

import os
import SimpleHTTPServer
import SocketServer
import threading
import settings

json_views = {}

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

def register(d):
    """
    Register json views.
    """
    global json_views
    json_views = {"/data/%s.json" % k: v for k, v in d.items()}

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in json_views:
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            json_views[self.path].write(self.wfile)
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
