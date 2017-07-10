"""
Module to hold application settings.
"""

import os 
from time import strftime

#: Width of cells in pixels
CELL_WIDTH = 32
#: Height of cells in pixels
CELL_HEIGHT = 32
#: Max draw FPS of the simulation
MAX_FPS = 60
#: Time per simulation step in miliseconds (a lower step time results in a faster simulation, 0 = equal to draw speed)
SIMULATION_STEP_TIME = 50

#: Port at which the internal web-server listens
WEB_LISTEN_PORT = 8080

# Do not edit below this line.
ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

AGENT_DIR = os.path.join(ROOT_DIR, "_agents")
WORLD_DIR = os.path.join(ROOT_DIR, "_worlds")
EXPERIMENT_DIR = os.path.join(ROOT_DIR, "_experiments")
SIMULATIONS_RENDERS_DIR = os.path.join(ROOT_DIR, "_renders")
SIMULATION_RENDERS_DIR = os.path.join(SIMULATIONS_RENDERS_DIR, strftime("%Y%m%dT%H%M%S"))
WEBROOT_DIR = os.path.join(ROOT_DIR, "webroot")
WEBROOT_DATA_DIR  = os.path.join(WEBROOT_DIR, "data")
