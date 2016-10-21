"""
Module to hold application settings.
"""

import os 
ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

CELL_WIDTH = 32
CELL_HEIGHT = 32
MAX_FPS = 25

LISTEN_PORT = 8418

WEB_LISTEN_PORT = 8080
WEBROOT_DIR = os.path.join(ROOT_DIR, "webroot")
WEBROOT_DATA_DIR  = os.path.join(WEBROOT_DIR, "data")
TRACE_FILE_PATH = os.path.join(WEBROOT_DATA_DIR, "traces.json")