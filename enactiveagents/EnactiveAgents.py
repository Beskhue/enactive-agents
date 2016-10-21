"""
Entry module of the application.
"""

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

    def run(self):
        """
        Process PyGame events until halt is true.
        """

        self.halt = False

        print("Starting heartbeat.")
        while not self.halt:
            AppState.get_state().get_event_manager().post_event(events.TickEvent())
            AppState.get_state().get_event_manager().post_event(events.DrawEvent())

            AppState.get_state().get_clock().tick(settings.MAX_FPS)

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

def main():
    """
    Main function of the application.
    """
    # Initialize the event manager.
    event_manager = events.EventManager()
    AppState.get_state().set_event_manager(event_manager)

    # Initialize and register the application heartbeat.
    heart_beat = HeartBeat()
    event_manager.register_listener(heart_beat)

    # Initialize and register the world.
    basic_experiment = experiment.basic.BasicVisionExperiment()
    world = basic_experiment.get_world()
    event_manager.register_listener(world)
    AppState.get_state().set_world(world)

    # Initialize pygame.
    surface = init()

    # Initialize and register the view.
    main_view = view.View(surface)
    event_manager.register_listener(main_view)

    # Initialize the website trace history view.
    trace_view = agentevents.AgentEvents(settings.TRACE_FILE_PATH)
    event_manager.register_listener(trace_view)

    # Initialize and register the controller.
    main_controller = controller.Controller()
    event_manager.register_listener(main_controller)

    # Start the webserver.
    webserver.trace_view = trace_view
    webserver.start()

    # Start the heartbeat.
    heart_beat.run()

if __name__ == '__main__':
    """
    Application entry-point.
    """

    main()
