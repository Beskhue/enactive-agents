"""
Module that holds classes that represent the world.
"""

import abc
import math
import pygame
import events
import agent

class World(events.EventListener):
    """
    Class that represents the world.
    """

    entities = []
    width = 20
    height = 20

    def __init__(self):
        pass

    def get_entities_at(self, position):
        entities = []
        for entity in self.entities:
            if entity.at(position):
                entities.append(entity)

        return entities

    def enact(self, agent, primitiveInteraction):
        """
        :param agent: The agent attempting to perform the primitive interaction.
        :type agent: Agent
        :param primitiveInteraction: The primitive interaction that is being 
                                     attempted to be performed.
        :type primitiveInteraction: PrimitiveInteraction
        :return: The primitiveInteraction that was actually enacted.
        """
        pass

    def collidable_entity_at(self, position):
        for entity in self.entities:
            if entity.collidable() and entity.at(position):
                return True
        return False

    def can_step(self, agent):
        position = Position(agent.get_position())
        position.add(agent.get_move_delta(1))
        return not collidable_entity_at(position)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_entities(self):
        return self.entities

    def add_entity(self, entity):
        self.entities.append(entity)

    def notify(self, event):
        for entity in self.entities:
            if isinstance(entity, agent.Agent):
                
                pass

class Position:
    
    x = 0
    y = 0

    def __init__(self, position=None):
        if not position is None:
            if isinstance(position, Position):
                self.x = position.x
                self.y = position.y
            else:
                self.x = position[0]
                self.y = position[1]

    def get(self):
        return (self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set(self, position):
        if not isinstance(position, Position):
            position = Position(position)

        self.x = position.x
        self.y = position.y

    def add(self, delta):
        self.x += delta[0]
        self.y += delta[1]

    def __eq__(self, other):
        if not isinstance(position, Position):
            position = Position(position)

        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not self == other

class Entity(object):
    """
    Class that represents an entity that can be placed in a world.

    The position of the entity is its top-left corner.
    """

    width = 1
    height = 1
    step_size = 0.01
    rect = None

    def __init__(self, position = None, rotation = 0):
        if position is None:
            self.position = Position()
        else:
            self.position = Position(position)
        self.rotation = rotation

    def get_position(self):
        return self.position

    def get_rotation(self):
        return self.rotation

    def set_position(self, position):
        self.position.set(position)

    def set_rotation(self, rotation):
        self.rotation = rotation

    def add_position(self, positionDelta):
        self.position.add(positionDelta)

    def add_rotation(self, rotationDelta):
        self.rotation += rotationDelta

    def at(self, position):
        """
        Test if this entity is at a certain position (i.e., the position is 
        inside the entity's rectangle).
        :param position: The position to check.
        :return: True if the position is inside the entity's rectangle.
        """
        if not isinstance(position, Position):
            position = Position(position)

        return inside(
            (
                self.position.get_x(),
                self.position.get_y(),
                self.width, 
                self.height
            ),
            position
        )

    def step(self):
        """
        Move the entity one step.
        """
        self.move(1)

    def move(self, steps):
        """
        Move the entity a certain number of steps.
        :param steps: The number of steps to move the agent.
        """
        self.position.add(self.get_move_delta(steps))

    def get_move_delta(self, steps):
        """
        Get the change in position if the agent were to move.
        :param steps: The number of steps the agent would move.
        """
        angle = math.radians(self.rotation)
        sine = math.sin(angle)
        cos = math.cos(angle)
        return (
            steps * self.step_size * cos, 
            -steps * self.step_size * sine
        )
        

    def collide(self, other):
        """
        Get whether this entity and the other entity or rect are intersecting.
        If other is a rect, it should be in the form of:
        [x, y, width, height]
        :param other: The entity or rect to check for collision with this entity.
        """
        if not self.collidable():
            return false

        if isinstance(other, Entity):
            return collide(
                (
                    self.position.get_x(),
                    self.position.get_y(),
                    self.width, 
                    self.height
                ),
                (
                    other.position.get_x(),
                    other.position.get_y(),
                    other.width, 
                    other.height
                )
            )
        else:
            return collide(
                (
                    self.position.get_x(),
                    self.position.get_y(),
                    self.width, 
                    self.height
                ), 
                other
            )

    def get_color(self):
        """
        Get the color of the entity.
        :return: The color of the entity.
        :rtype: (int, int, int, int)
        """
        if hasattr(self, 'color'):
            return self.color
        else:
            return (255,255,255,255)

    def set_color(self, color):
        """
        Set the color of the entity.
        :param color: The color to set the entity to.
        :type color: (int, int, int, int)
        """
        self.color = color

    @abc.abstractmethod
    def collidable(self):
        """
        Return whether entities can collide with this object.
        :return: True if entities can collide with this object, false otherwise.
        :rtype: bool
        """
        raise NotImplementedError("Should be implemented in child")

def collide(r1, r2):
    return not (
        r2[0] > r1[0]+r1[2] or
        r2[0]+r2[2] < r1[0] or
        r2[1] > r1[1]+r1[3] or
        r2[1]+r2[3] < r1[1]
    )

def inside(r, p):
    return not (
        p.get_x() < r[0] or
        p.get_y() > r[1] or
        p.get_x() > r[0] + r[2] or
        p.get_y() > r[1] + r[3]
    )