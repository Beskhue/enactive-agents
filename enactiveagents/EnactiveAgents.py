"""
Entry module of the application.
"""

import os 
import sys
from time import strftime
import json

import pygame
from appstate import AppState
import settings
import events
from view import view
from view import agentevents
from controller import controller
import experiment.basic
import webserver

class HeartBeat(events.EventListener):
    """
    Class implementing the heartbeat of the application.
    """

    def run(self, slow = True, halt_fun = None, metrics_fun = None):
        """
        Process PyGame events until halt is true.

        :param slow: whether the simulation should be slowed for
                     visible ticks and renders.
        :param halt_fun: A callable taking as input the current
                         simulation time in ticks, and returning
                         a boolean indicating whether the simulation
                         should halt.
        :param metrics_fun: A callable returning a dictionary of named
                            metrics.
        """

        self.metrics = []

        self.halt = False

        print("Starting heartbeat.")
        time_elapsed = 0
        while not self.halt:
            if callable(halt_fun) and halt_fun(AppState.get_state().get_t()):
                self.halt = True
                continue

            AppState.get_state().get_event_manager().post_event(events.ControlEvent())

            ticked = False
            
            if not slow or (AppState.get_state().is_running() and time_elapsed >= settings.SIMULATION_STEP_TIME):
                AppState.get_state().get_logger().info("------- t = %s" % AppState.get_state().get_t())

                AppState.get_state().get_event_manager().post_event(events.TickEvent())
                time_elapsed = 0
                ticked = True

                if callable(metrics_fun):
                    self.metrics.append(metrics_fun())

            AppState.get_state().get_event_manager().post_event(events.DrawEvent(ticked and AppState.get_state().get_save_simulation_renders()))

            if slow:
                time_elapsed += AppState.get_state().get_clock().tick(settings.MAX_FPS)

            if ticked:
                AppState.get_state().increment_t()

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self.halt = True

def init():
    """
    Initialize pygame.

    :returns: The surface of the pygame display.
    """

    print("Loading pygame modules.")
    pygame.display.init()
    AppState.get_state().set_clock(pygame.time.Clock())
    flags = pygame.DOUBLEBUF
    surface = pygame.display.set_mode(
        (
            AppState.get_state().get_world().get_width() * settings.CELL_WIDTH,
            AppState.get_state().get_world().get_height() * settings.CELL_HEIGHT,
        ), 
        flags)
    surface.set_alpha(None)
    pygame.display.set_caption('Enactive Agents v2')

    return surface

def run_experiment(experiment_, render = True, interactive = True, console_output = True, save_logs = True):
    """
    Run an experiment until it halts. Simulates the world defined 
    by the experiment and handles control events.
    
    :param experiment_: An object of type Experiment.
    :param render: A boolean indicating whether the simulation is
                   to be rendered to the screen.
    :param interactive: A boolean indicating whether interactive
                        is to be enabled. If interactive mode is
                        on, rendering should be on as well.
    :param console_output: A boolean indicating whether simulation
                           output is to be displayed in the console.
    :param save_logs: A boolean indicating whether simulation output
                      is to be saved in a log file.
    """

    if interactive:
        assert render, "render must be true if interactive mode is set"

    # Reset the app state
    AppState.get_state().reset()

    # Initialize the event manager.
    event_manager = events.EventManager()
    AppState.get_state().set_event_manager(event_manager)

    # Initialize and register the application heartbeat.
    heart_beat = HeartBeat()
    event_manager.register_listener(heart_beat)

    # Initialize and register the world.
    AppState.get_state().set_experiment(experiment_)
    world = experiment_.get_world()
    event_manager.register_listener(world)
    AppState.get_state().set_world(world)

    # Initialize pygame.
    surface = init()

    if render:
        # Initialize and register the view.
        main_view = view.View(surface)
        event_manager.register_listener(main_view)

    # Initialize the website trace history view.
    trace_view = agentevents.AgentEvents()
    event_manager.register_listener(trace_view)

    # Initialize and register the controller.
    main_controller = controller.Controller()
    event_manager.register_listener(main_controller)

    if interactive:
        # Add the experiment controller to the controller
        main_controller.set_experiment_controller(lambda e, coords: experiment_.controller(e, main_view.window_coords_to_world_coords(coords)))

    if console_output:
        # Enable console logger
        AppState.get_state().enable_console_logger()

    if save_logs:
        # Store experiment logs
        if not os.path.isdir(settings.RESULTS_DIR):
            os.makedirs(settings.RESULTS_DIR)
        file_path = os.path.join(settings.RESULTS_DIR, "%s - %s.log" % (strftime("%Y%m%dT%H%M%S"), experiment_.__class__.__name__))
        AppState.get_state().enable_file_logger(file_path)

    # Start the webserver.
    webserver.register({'traces': trace_view})
    webserver.start()

    # Start the heartbeat.
    heart_beat.run(slow = render, halt_fun = experiment_.halt, metrics_fun = experiment_.calculate_metrics)

    if len(heart_beat.metrics) > 0:
        # Store experiment results
        if not os.path.isdir(settings.RESULTS_DIR):
            os.makedirs(settings.RESULTS_DIR)

        file_path = os.path.join(settings.RESULTS_DIR, "%s - %s.json" % (strftime("%Y%m%dT%H%M%S"), experiment_.__class__.__name__))
        with open(file_path, 'w') as f:
            json.dump(heart_beat.metrics, f, indent=4, sort_keys=True)
    
def main():
    """
    Main function of the application.
    """

    experiments = []
    experiments.append(experiment.basic.BasicRandomExperiment())
    experiments.append(experiment.basic.BasicVisionExperiment())

    for experiment_ in experiments:
        run_experiment(experiment_, render = True, interactive = True, console_output = True, save_logs = True)

if __name__ == '__main__':
    """
    Application entry-point.
    """

    main()
