"""
Main world view.
"""

import abc
import events
import pygame
import model
from appstate import AppState

class View(events.EventListener):
    """
    View class.
    """

    sprites = {}

    def __init__(self, surface):
        """
        Initialize the view.

        :param surface: The surface of the view.
        """
        self.surface = surface
        self.group = pygame.sprite.RenderUpdates()

    def draw_entities(self):
        """
        Draw all the entities in the world onto the canvas.
        """
        world = AppState.get_state().get_world()
        
        # Create sprites for entities we do not have sprites for yet
        for entity in AppState.get_state().get_world().get_entities():
            if entity not in self.sprites.keys():
                self.sprites[entity] = Sprite(entity, self)
                self.group.add(self.sprites[entity])
        # Remove sprites for entities that were removed
        for entity in self.sprites.keys():
            if entity not in AppState.get_state().get_world().get_entities():
                self.group.remove(self.sprites[entity])
                del self.sprites[entity]
        
        self.group.draw(self.surface)

    def get_cell_width(self):
        """
        Get the width of a cell on the canvas.
        :return: The width of a single cell on the canvas.
        :rtype: int
        """
        return round(float(self.surface.get_width()) / AppState.get_state().get_world().get_width())
    
    def get_cell_height(self):
        """
        Get the height of a cell on the canvas.
        :return: The height of a single cell on the canvas.
        :rtype: int
        """
        return round(float(self.surface.get_height()) / AppState.get_state().get_world().get_height())

    def draw(self):
        """
        Draw the world.
        """
        self.surface.fill([0,0,0])
        self.surface.convert()
        self.draw_entities()
        pygame.display.flip()

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            self.draw()


class Sprite(pygame.sprite.Sprite):
    """
    Class to represent world entities as sprites.
    """

    def __init__(self, entity, view):
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        self.view = view
        self.shape = self.get_shape()

        # Scale the sprite's shape
        shape = []
        for s in self.get_shape():
            shape.append([
                s[0] * self.view.get_cell_width(),
                s[1] * self.view.get_cell_height()
            ])

        # Create the surface (image) of the sprite
        self.surface = pygame.Surface([self.view.get_cell_width(), self.view.get_cell_height()])
        self.surface.set_colorkey((255, 0, 0))

        # Draw the shape onto the surface
        pygame.draw.polygon(
            self.surface, 
            self.entity.get_color(), 
            shape,
            0)


    def get_shape(self):
        """
        Get the shape of the sprite.
        :return: The shape of the sprite as a list of vertices.
        :rtype: list
        """
        if isinstance(self.entity, model.agent.Agent):
            return [[.2, .25], [.2, .75], [.85, 0.5]]
        else:
            return [[0,0], [0,1], [1,1], [1,0], [0,0]]


    @property 
    def rect(self):
        """
        Get the rectangle of the sprite (i.e., its bounding box in canvas
        coordinates).
        """
        return pygame.Rect(
            self.entity.get_position().get_x() * self.view.get_cell_width(), 
            self.entity.get_position().get_y() * self.view.get_cell_height(), 
            self.view.get_cell_width(),
            self.view.get_cell_height()
        )

    @property
    def image(self):
        """
        Get the image of the sprite.
        """
        if self.entity.get_rotation() != 0:
            surface = rot_center(self.surface, self.entity.get_rotation())
            return surface
        else:
            return self.surface

def rot_center(image, angle):
    """
    Rotate a surface around its center
    """

    original_rect = image.get_rect()
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = original_rect.copy()
    rotated_rect.center = rotated_image.get_rect().center
    rotated_image = rotated_image.subsurface(rotated_rect).copy()
    return rotated_image