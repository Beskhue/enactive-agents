"""
Main world view.
"""

import abc
import os
import math
import events
import pygame
import model
from appstate import AppState
import settings

class View(events.EventListener):
    """
    View class.
    """

    sprites = {}
    agent_interaction = {}
    created_renders_dir = False

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

    def draw_mouse_highlight(self):
        """
        Draw an indication of where the mouse is on the canvas.
        """
        if pygame.mouse.get_focused():
            cell = self.window_coords_to_world_coords(pygame.mouse.get_pos())
            rect = (cell[0]*self.get_cell_width(), cell[1]*self.get_cell_height(), self.get_cell_width(), self.get_cell_height());
            pygame.draw.rect(self.surface, (255,125,55,255), rect, 1);

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

    def window_coords_to_world_coords(self, coords):
        """
        Transform window pixel coordinates to world coordinates
        :param coords: Window pixel coords
        :return: World coordinates
        """
        if coords:
            return (math.floor(coords[0] / self.get_cell_width()), math.floor(coords[1] / self.get_cell_height()))
        else:
            return None

    def draw(self, save_to_file):
        """
        Draw the world.
        """
        self.surface.fill([0,0,0])
        self.surface.convert()
        self.draw_entities()
        self.draw_mouse_highlight()
        pygame.display.flip()

        if save_to_file:
            self.save_surface_to_file()

    def save_surface_to_file(self):
        # Create output directory if it does not exist
        if not self.created_renders_dir and not os.path.exists(settings.SIMULATION_RENDERS_DIR):
            os.makedirs(settings.SIMULATION_RENDERS_DIR)
            self.created_renders_dir = True

        path = os.path.join(settings.SIMULATION_RENDERS_DIR, "t%s.png" % AppState.get_state().get_t())
        pygame.image.save(self.surface, path)

    def notify(self, event):
        if isinstance(event, events.AgentEnactionEvent):
            self.agent_interaction[event.agent] = event.action
        elif isinstance(event, events.DrawEvent):
            self.draw(event.get_save_to_file())


class Sprite(pygame.sprite.Sprite):
    """
    Class to represent world entities as sprites.
    """

    def __init__(self, entity, view):
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        self.view = view

        self.color = self.get_color()
        self.store_image()

    def store_image(self):
        """
        The the image of the sprite on a surface.
        """
        # Create the surface (image) of the sprite
        self.surface = pygame.Surface([self.entity.get_width() * self.view.get_cell_width(), self.entity.get_height() * self.view.get_cell_height()])
        self.surface.set_colorkey((0, 0, 0))

        # Scale the sprite's shape
        self.shape = []
        for s in self.get_shape():
            self.shape.append([
                s[0] * self.view.get_cell_width(),
                s[1] * self.view.get_cell_height()
            ])

        # Draw the shape onto the surface
        pygame.draw.polygon(
            self.surface, 
            self.color, 
            self.shape,
            0)

    def get_color(self):
        """
        Get the color the sprite should be. The color can change, e.g. depending
        on the interaction an agent has just enacted.
        :return: The color the sprite should be
        """
        color = self.entity.get_color()
        if self.entity in self.view.agent_interaction:
            interaction = self.view.agent_interaction[self.entity]
            if isinstance(interaction, model.interaction.PrimitivePerceptionInteraction):
                interaction = interaction.get_primitive_interaction()
            if interaction.get_name() == "Step" and interaction.get_result() == "Fail":
                color = (255,0,0,255)
        return color

    def get_surface(self):
        """
        Get the surface (image) of the sprite. Update the surface if the color
        of the sprite has to change.
        :return: The surface (image) of the sprite.
        """
        color = self.get_color()
        if color != self.color:
            self.color = color
            self.store_image()
        return self.surface

    def get_shape(self):
        """
        Get the shape of the sprite.
        :return: The shape of the sprite as a list of vertices.
        :rtype: list
        """
        if isinstance(self.entity, model.agent.Agent):
            return [[.2, .25], [.2, .75], [.85, 0.5]]
        elif isinstance(self.entity, model.structure.Block) or isinstance(self.entity, model.structure.Food):
            return [
                [0.35,0.35], 
                [0.35, self.entity.get_height() - 1 + 0.65], 
                [self.entity.get_width()- 1 + 0.65, self.entity.get_height() - 1 + 0.65], 
                [self.entity.get_width() - 1 + 0.65, 0.35], 
                [0.35,0.35]
            ]
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
        surface = self.get_surface()
        if self.entity.get_rotation() != 0:
            surface = rot_center(surface, self.entity.get_rotation())
            return surface
        else:
            return surface

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