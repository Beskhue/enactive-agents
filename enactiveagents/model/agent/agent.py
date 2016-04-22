"""
Module that holds classes that represent agents.
"""

import pygame
import model.world

class Agent(model.world.Entity):
    """
    Class that represents an agent.
    """

    color = (3, 124, 146, 255)
    interactions = []

    def __init__(self):
        super(Agent, self).__init__()

    def select_interaction(self):
        """
        Select an interaction to enact.

        :return: 
        """
        pass

    def enact_interaction(self, interaction):
        """
        :param interaction: The interaction to enact.
        :type interaction: Interaction
        """ 
        pass

    def set_primitives(self, primitives):
        self.primitives = primitives

    def set_motivation(self, motivation):
        self.motivation = motivation

    def set_enact_logic(self, enact_logic):
        self.enact_logic = enact_logic

    def collidable(self):
        return False