"""
Entry module of the application.
"""

import pygame
from appstate import AppState
import settings
import events
from view import view
from controller import controller

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
            event = events.TickEvent()
            AppState.get_state().get_event_manager().post_event(event)
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
    surface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption('Enactive Agents v2')

    return surface

def main():
    """
    Main function of the application.
    """
    # Initialize the event manager.
    eventManager = events.EventManager()
    AppState.get_state().set_event_manager(eventManager)

    # Initialize and register the application heartbeat.
    heartBeat = HeartBeat()
    eventManager.register_listener(heartBeat)

    # Initialize pygame.
    surface = init()

    # Initialize and register the view.
    mainView = view.View(surface)
    eventManager.register_listener(mainView)

    # Initialize and register the controller.
    mainController = controller.Controller()
    eventManager.register_listener(mainController)

    # Start the heartbeat.
    heartBeat.run()

if __name__ == '__main__':
    """
    Application entry-point.
    """

    main()
