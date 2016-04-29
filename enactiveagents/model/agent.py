"""
Module that holds classes that represent agents.
"""

import abc
import random
import pygame
import world
import interaction
import interactionmemory

class Agent(world.Entity):
    """
    Class that represents an agent.
    """

    color = (3, 124, 146, 255)

    def __init__(self):
        super(Agent, self).__init__()
        self.setup_interaction_memory()

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

    @abc.abstractmethod
    def setup_interaction_memory(self):
        """
        Setup the interaction memory of this agent.
        """
        raise NotImplementedError("Should be implemented by child.")

    def set_primitives(self, primitives):
        for primitive in primitives:
            self.interaction_memory.add_interaction(primitive)

    def set_motivation(self, motivation):
        for primitive, valence in motivation.iteritems():
            self.interaction_memory.set_valence(primitive, valence)

    def collidable(self):
        return False

class SimpleAgent(Agent):
    """
    An agent with a simple existence.
    """
    enacted = None

    def anticipate(self):
        """
        Anticipate the possible interactions based on the current context.
        :return: A list of possible (primitive) interactions.
        """
        interactions = []
        for composite_interaction in self.interaction_memory.get_composite_interactions():
            if composite_interaction.get_pre() == self.enacted:
                interactions.append(composite_interaction.get_post())

        return interactions

    def select_experiment(self, anticipations):
        """
        Select the best interaction from a list of anticipated interactions.

        If the list of anticipated interactions is empty or if the best 
        interaction has negative valence, return a random primitive interaction.

        :param anticipations: The list of interactions to choose an experiment
        from.

        :return: A chosen primitive interaction.
        """
        anticipations.sort(
            key = lambda x: self.interaction_memory.get_valence(x),
            reverse = True
        )
        if len(anticipations) > 0 and self.interaction_memory.get_valence(anticipations[0]) > 0:
            return anticipations[0]
        else:
            return random.choice(self.interaction_memory.get_primitive_interactions())

    def learn_composite_interaction(self, context, enacted):
        """
        Learn a composite interaction or reinforce it if it is already known.

        :param context: The context (pre-interaction).
        :param enacted: The newly enecated interaction (post-interaction).
        """
        composite = interaction.CompositeInteraction(context, enacted)
        if composite not in self.interaction_memory.get_composite_interactions():
            self.interaction_memory.add_interaction(composite)
        else:
            self.interaction_memory.increment_weight(composite)

    def prepare_interaction(self):
        anticipations = self.anticipate()
        experiment = self.select_experiment(anticipations)
        return experiment

    def enacted_interaction(self, interaction, data):
        if not self.enacted is None:
            self.learn_composite_interaction(self.enacted, interaction)
        self.enacted = interaction

    def setup_interaction_memory(self):
        self.interaction_memory = interactionmemory.InteractionMemory()

class ConstructiveAgent(Agent):
    """
    An agent with a fully recursive existence. It considers all experiment as 
    abstract and processes all experiments in the same way.
    """
    def setup_interaction_memory(self):
        pass

    def prepare_interaction(self):
        pass

    def enacted_interaction(self, interaction, data):
        pass