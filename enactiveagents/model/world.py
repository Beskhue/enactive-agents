"""
Module that holds classes that represent the world.
"""

import abc
import collections
from random import shuffle
import pygame
import events
import interaction
import agent
from entity import Position

class World(events.EventListener):
    """
    Class that represents the world.
    """

    def __init__(self):
        self.entities = []
        self.enact_logic = {}
        self.complex_enact_logic = []
        self.width = 20
        self.height = 20
        self.position_entity_map = False
        self.position_entity_map = {}

    def get_entities_at(self, position):
        if self.position_entity_map_valid:
            if position in self.position_entity_map:
                return self.position_entity_map[position]
            else:
                return []
        else:
            entities = []

            for entity in self.entities:
                if entity.at(position):
                    entities.append(entity)

            return entities

    def build_position_entity_map(self):
        """
        Builds the position-entity map. This is used for fast lookup of
        entitiy positions.
        """
        self.position_entity_map.clear()

        for entity in self.entities:
            positions = entity.get_spanning_positions()
            for pos in positions:
                if pos not in self.position_entity_map:
                    self.position_entity_map[pos] = []

                self.position_entity_map[pos].append(entity)

        self.position_entity_map_valid = True 

    def get_entities_in_front(self, entity):
        """
        Get the entities that are in front of the given entity.
        """
        pos = Position(entity.get_position())
        pos.add(entity.get_move_delta())
        return self.get_entities_at(pos)

    def collidable_entity_at(self, position):
        for entity in self.get_entities_at(position):
            if entity.collidable():
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
        """
        Get all entities (structures and agents) in the world
        :return: All entities in the world
        """
        return self.entities

    def get_agents(self):
        """
        Get all agent entities in the world
        :return: All agent entities in the world
        """
        # import agent
        return [entity for entity in self.entities if isinstance(entity, agent.Agent)]

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
        for agent_, (interaction_, data) in agents_data.iteritems():
            # Get enact logic
            if isinstance(interaction_, interaction.PrimitivePerceptionInteraction):
                primitive_interaction = interaction_.get_primitive_interaction()
            else:
                primitive_interaction = interaction_

            agents_data[agent_] = (primitive_interaction, data)

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
        for agent_, (primitive_interaction, data) in agents_data.iteritems():
            if agent_ in enacted:
                # Agent has already been handled
                continue

            action = primitive_interaction.get_name()

            if action in self.enact_logic[agent_]:
                callback = self.enact_logic[agent_][action]
                
                # Process logic and get actual enacted interaction
                enacted_interaction = callback(self, agent_, primitive_interaction)
            else:
                # There is no logic registered with this interaction,
                # do nothing.
                enacted_interaction = primitive_interaction
            
            # Tell agent which interaction was enacted
            enacted[agent_] = enacted_interaction

        # Notify agents of which interaction was enacted
        for agent_, (primitive_interaction, data) in agents_data.iteritems():
            if agent_.has_perception_handler() and not isinstance(enacted[agent_], interaction.PrimitivePerceptionInteraction):
                # The agent has a perception handler, and the enacted 
                # interaction is not yet a primitive perception interaction, so
                # get and add the percept
                agent_.enacted_interaction(interaction.PrimitivePerceptionInteraction(enacted[agent_], agent_.get_perception(self)), data)
            else:
                agent_.enacted_interaction(enacted[agent_], data)

    def notify(self, event):
        # import agent
        if isinstance(event, events.TickEvent):
            agents = []
            for entity in self.entities:
                if isinstance(entity, agent.Agent):
                    agents.append(entity)
            shuffle(agents)

            # Build the position entity map to make entity_at lookup quick
            self.build_position_entity_map()
            agents_data = self.prepare(agents)
            
            # Agents will now enact in (and mutate) the world, so invalidate
            # the entity map
            self.position_entity_map_valid = False

            self.enact(agents_data)
