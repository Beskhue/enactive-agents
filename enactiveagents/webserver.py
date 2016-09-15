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

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", settings.WEB_LISTEN_PORT), handler)
    httpd.serve_forever()