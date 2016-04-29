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
        manipulating the world state, and afterwards all these interactions
        are enacted (in randomized order). The world notifies the agent
        of which interaction was actually enacted.
        
        This ensures that an agent does not have access to world state 
        information it should not yet know at any point in time (especially 
        when it becomes more complex with e.g. a visual subsystem). If 
        preparation was immediately followed by enaction, an agent could
        potentially respond to the interaction of another agent made "earlier"
        at the same discrete point in time!

        :return: The primitive interaction that is to be enacted and optionally
        something that will be passed to enacted_interaction of this agent.
        """
        raise NotImplementedError("Should be implemented by child.")

    @abc.abstractmethod
    def enacted_interaction(self, interaction, data):
        """
        Tell the agent which primitive interaction was actually enacted. 

        :param interaction: The primitive interaction that was actually
        enacted.
        :param data: The data that was (optionally) returned by 
        prepare_interaction this step.
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
        return self.primitives[1]

    def enacted_interaction(self, interaction, data):
        pass

class ConstructiveAgent(Agent):
    """
    An agent with a fully recursive existence. It considers all experiment as 
    abstract and processes all experiments in the same way.
    """
    def prepare_interaction(self):
        pass

    def enacted_interaction(self, interaction, data):
        pass