"""
Module that holds classes that represent agents.
"""

import abc
import pygame
import world
import interaction

class Agent(world.Entity):
    """
    Class that represents an agent.
    """

    color = (3, 124, 146, 255)
    interactions = []

    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def prepare_interaction(self):
        """
        Prepare an interaction to enact. 
        
        Interaction enaction is split into two parts to better handle multiple
        agents. First, all agents prepare the interaction to enact without
        manipulating the world state, and afterwards all agents (in randomized 
        order) enact that interaction. 
        
        This ensures that an agent at any one point in time does not have
        access to world state information it should not yet know (especially 
        when it becomes more complex with e.g. a visual subsystem). If 
        preparation was immediately followed by enaction, an agent could
        potentially respond to the interaction of another agent made "earlier"
        at the same discrete point in time!

        :return: Something that will be passed to enact_interaction of this
        agent.
        """
        raise NotImplementedError("Should be implemented by child.")

    @abc.abstractmethod
    def enact_interaction(self, data):
        """
        Enact the interaction that was prepared.

        :param data: The data that was returned by prepare_interaction this 
        step.

        :return: The interaction the agent wishes to enact.
        :rtype: model.interaction.Interaction
        """ 
        raise NotImplementedError("Should be implemented by child.")

    def set_primitives(self, primitives):
        self.primitives = primitives

    def set_motivation(self, motivation):
        self.motivation = motivation

    def collidable(self):
        return False

class SimpleAgent(Agent):
    """
    An agent with a simple existence.
    """
    def prepare_interaction(self):
        pass

    def enact_interaction(self, data):
        pass

class ConstructiveAgent(Agent):
    """
    An agent with a fully recursive existence. It considers all experiment as 
    abstract and processes all experiments in the same way.
    """
    def prepare_interaction(self):
        pass

    def enact_interaction(self, data):
        pass