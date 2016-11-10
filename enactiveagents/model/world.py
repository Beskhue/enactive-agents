"""
Module that holds classes that represent the world.
"""

import abc
import math
import collections
from random import shuffle
import pygame
import events
import interaction
import agent

class World(events.EventListener):
    """
    Class that represents the world.
    """

    entities = []
    enact_logic = {}
    complex_enact_logic = []
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

    def entity_rect_collision(self, rect):
        for entity in self.entities:
            if entity.collidable() and entity.collide(rect):
                return True
        return False

    def can_step(self, agent):
        position = Position(agent.get_position())
        position.add(agent.get_move_delta(1))
        return not self.entity_rect_collision(
            (
                position.get_x(), 
                position.get_y(), 
                agent.get_width(), 
                agent.get_height()
            )
        )

    def add_enact_logic(self, agent, callback_dict):
        """
        Set the enact logic for a given agent. callback_dict is a dictionary
        (map) of primitive interactions to callbacks. The callbacks will be
        called when the agent attempts to enact a certain (primitive) 
        interaction. The callback receives as parameters an intance of the
        world, the agent and the primitive interaction that was enacted.

        The callback should manipulate the world state (e.g., move the agent)
        and return the primitive interaction that was interacted (potentially
        different from the interaction that was intended to be interacted).
        """
        self.enact_logic[agent] = callback_dict

    def add_complex_enact_logic(self, callback, action = None):
        """
        Add a complex enact logic callback. The callback will be called
        when all agents have prepared their interaction. The callback receives
        an instance of the world and a mapping of all agents to their prepared
        interactions.

        The callback can handle on zero, one, or more agents present in the mapping.
        Not all agents have to be handled by the callback. The callback should
        manipulate the world state (e.g., move one or more agents) and it should
        return a mapping of agents to primitive interactions the agents have
        actually enacted for each agent the callback handled.

        Multiple complex callbacks can be registered. The callbacks are processed
        in a first-come first-out basis (i.e., callbacks registered first will
        process interactions first).

        :param callback: The callable to add
        :param action: Optional, if set the callback will only receive agents
                       trying to enact the interaction with the given action
        """
        if action == None:
            self.complex_enact_logic.append(callback)
        else:
            self.complex_enact_logic.append((callback, action))

    def remove_complex_enact_logic(self, callback):
        """
        :param callback: The callable to remove
        """
        self.complex_enact_logic = [x for x in self.complex_enact_logic if not (x == callback or (isinstance(x, tuple) and x[0] == callback))]

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

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def prepare(self, agents):
        """
        Let all agents prepare their next interaction. Store the interaction
        they wish to enact and any potential (optional) data the agents return.

        :param agents: The agents to have prepare their interactions.
        :return: A dictionary of agents mapping to a tuple with the interaction
                 they wish to enact and the data returned by their preparation 
                 (this data is to be delivered back to the agents (unmutated) 
                 when they are told which interaction was enacted).
        """
        agents_data = {}
        for agent in agents:
            val = agent.prepare_interaction()
            if isinstance(val, interaction.PrimitiveInteraction) or isinstance(val, interaction.PrimitivePerceptionInteraction):
                agents_data[agent] = (val, None)
            elif isinstance(val, collections.Sequence) and len(val) == 2 and (isinstance(val[0], interaction.PrimitiveInteraction) or isinstance(val[0], interaction.PrimitivePerceptionInteraction)):
                agents_data[agent] = (val[0], val[1])
            else:
                raise ValueError("Expected the return value of prepare_interaction to be a primitive interaction or a sequence of an interaction and data.")

        return agents_data
            
    def enact(self, agents_data):
        """
        Let all agents enact their prepared interaction.

        :param agents_data: The agent and data mapping as generated in 
                            self.prepare.
        """

        enacted = {}

        # Get primitive interactions
        for agent, (interaction_, data) in agents_data.iteritems():
            # Get enact logic
            if isinstance(interaction_, interaction.PrimitivePerceptionInteraction):
                primitive_interaction = interaction_.get_primitive_interaction()
            else:
                primitive_interaction = interaction_

            agents_data[agent] = (primitive_interaction, data)

        # Execute complex interaction logic
        for callback in self.complex_enact_logic:
            if isinstance(callback, tuple):
                (callback, action) = callback
                # Get a mapping of agents to the intended primitive interactions, 
                # and filter out all primitives that do not correspond to the given action
                agents_interactions = {agent: primitive_interaction for agent, (primitive_interaction, data) in agents_data.items() if primitive_interaction.get_name() == action}
            else:
                # Get a mapping of agents to the intended primitive interactions
                agents_interactions = {agent: primitive_interaction for agent, (primitive_interaction, data) in agents_data.items()}
            
            if len(agents_interactions) > 0:
                enacted_ = callback(self, agents_interactions)
                enacted.update(enacted_)

        # Execute interactions
        for agent, (primitive_interaction, data) in agents_data.iteritems():
            if agent in enacted:
                # Agent has already been handled
                continue

            action = primitive_interaction.get_name()

            if action in self.enact_logic[agent]:
                callback = self.enact_logic[agent][action]
                
                # Process logic and get actual enacted interaction
                enacted_interaction = callback(self, agent, primitive_interaction)
            else:
                # There is no logic registered with this interaction,
                # do nothing.
                enacted_interaction = interaction_
            
            # Tell agent which interaction was enacted
            enacted[agent] = enacted_interaction

        # Notify agents of which interaction was enacted
        for agent, (primitive_interaction, data) in agents_data.iteritems():
            agent.enacted_interaction(enacted[agent], data)

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            agents = []
            for entity in self.entities:
                if isinstance(entity, agent.Agent):
                    agents.append(entity)
            shuffle(agents)
            agents_data = self.prepare(agents)
            self.enact(agents_data)



class Position:
    
    x = 0
    y = 0
    PRECISION = 5

    def __init__(self, position=None):
        if not position is None:
            if isinstance(position, Position):
                self.x = Position.round(position.x)
                self.y = Position.round(position.y)
            else:
                self.x = Position.round(position[0])
                self.y = Position.round(position[1])

    @staticmethod
    def round(n):
        return round(n, Position.PRECISION)

    def get(self):
        return (self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set(self, position):
        if not isinstance(position, Position):
            position = Position(position)

        self.x = Position.round(position.x)
        self.y = Position.round(position.y)

    def add(self, delta):
        self.x = Position.round(self.x + delta[0])
        self.y = Position.round(self.y + delta[1])

    def __eq__(self, other):
        if not isinstance(other, Position):
            other = Position(other)

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
    step_size = 1
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

    def get_rect(self):
        return (self.position.get_x(), self.position.get_y(), width, height)

    def set_position(self, position):
        self.position.set(position)

    def set_rotation(self, rotation):
        self.rotation = rotation % 360

    def add_position(self, positionDelta):
        self.position.add(positionDelta)

    def add_rotation(self, rotationDelta):
        self.rotation += rotationDelta
        self.rotation = self.rotation % 360

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

    def get_move_delta(self, steps = 1):
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

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    @abc.abstractmethod
    def collidable(self):
        """
        Return whether entities can collide with this object.
        :return: True if entities can collide with this object, false otherwise.
        :rtype: bool
        """
        raise NotImplementedError("Should be implemented in child")

def collide(r1, r2):
    """
    Test if two rectangles collide.
    :param r1: The first rectangle.
    :param r2: The second rectangle.
    """
    return not (
        r2[0] >= r1[0]+r1[2] or # Left side of r2 is to the right of right side of r1
        r2[0]+r2[2] <= r1[0] or # Right side of r2 is to the left of left side of r1
        r2[1] >= r1[1]+r1[3] or # Top of r2 is below of bottom of r1
        r2[1]+r2[3] <= r1[1] # Bottom of r2 is above top of r1
    )

def inside(r, p):
    """
    Test if a point is inside a rectangle.
    :param r: The rectangle.
    :param p: The point.
    """
    return not (
        p.get_x() < r[0] or
        p.get_y() < r[1] or
        p.get_x() >= r[0] + r[2] or
        p.get_y() >= r[1] + r[3]
    )