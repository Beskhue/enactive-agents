"""
Main world view.
"""

import abc
import events
import pygame

class View(events.EventListener):
    """
    View class.
    """

    def __init__(self, surface):
        """
        Initialize the view.

        :param surface: The surface of the view.
        """
        self.surface = surface

    def draw_map(self):
        self.surface.fill([255,1,255])
        self.surface.convert()

    def draw_agents(self):
        pass

    def draw(self):
        self.draw_map()
        self.draw_agents()
        pygame.display.flip()

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            self.draw()


