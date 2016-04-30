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
                 something that will be passed to enacted_interaction of this 
                 agent.
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

    def __init__(self):
        super(ConstructiveAgent, self).__init__()
        self.enacting_interaction = False
        self.enacting_interaction_step = 0
        self.enacting_interaction_sequence = []
        self.enacted_sequence = []
        self.context = []

    def activate_interactions(self):
        """
        Step 1 of the sequential system.

        Known composite interactions whose pre-interaction belongs to the 
        context are activated.
        """
        activated = []
        for composite_interaction in self.interaction_memory.get_composite_interactions():
            if composite_interaction.get_pre() in self.context:
                activated.append(composite_interaction)

        return activated

    def propose_interactions(self):
        """
        Step 2 of the sequential system.

        Post-interactions of activated interactions are proposed, in order of
        the weights of the original activated interactions.
        """
        activated = self.activate_interactions()

        # TODO: this sort is unnecessary as the propositions are also sorted in
        # select_intended_interaction.
        activated.sort(
            key = lambda x: self.interaction_memory.get_weight(x), 
            reverse = True
        )
        proposed = map(lambda interaction: interaction.get_post(), activated)

        return proposed

    def select_intended_interaction(self):
        """
        Step 3 of the sequential system.

        The decisional mechanism; choose an interaction to enact (primitive
        or composite).

        The intended interaction is selected from the proposed interactions
        based on the weight of the propositions and the values of the proposed
        interactions.
        """
        proposed = self.propose_interactions()
        proposed.sort(
            key = lambda x: self.interaction_memory.get_proclivity(x), 
            reverse = True
        )
        if len(proposed) > 0 and self.interaction_memory.get_proclivity(proposed[0]) > 0:
            return proposed[0]
        else:
            # TODO: in Katja's implementation the activated interactions contain
            # some set of default interactions. The paper itself does not seem 
            # to mention how to deal with an empty activated set.
            return random.choice(self.interaction_memory.get_primitive_interactions())

    def update_context(self, enacted_interaction, learned_or_reinforced):
        """
        Step 6 of the sequential system.

        Update the context of the agent. The new context includes the enacted
        interaction (e_d), the post-interaction of e_d if it exists, and the
        interactions that were just learned or reinforced and that pass a 
        certain weight ("stabilized" interactions).

        :param enacted_interaction: The interaction that was enacted (can be
                                    different from the intended interaction)
        :param learned_or_reinforced: A list of interactions that were just
                                      learned or reinforced.
        """
        self.context = []

        for interaction_ in learned_or_reinforced:
            if self.interaction_memory.get_weight(interaction_) > 10:
                self.context.append(interaction_)

        if isinstance(enacted_interaction, interaction.CompositeInteraction):
            self.context.append(enacted_interaction.get_post())

        self.context.append(enacted_interaction)

    def prepare_interaction(self):
        if not self.enacting_interaction:
            # Decisional mechanism.
            # We are not currently enacting the primitives in a sequence of
            # interactions. Choose a new interaction to enact (steps 1-3).
            self.enacting_interaction = True
            self.enacting_interaction_step = 0
            self.enacted_sequence = []

            self.intended_interaction = self.select_intended_interaction()
            self.enacting_interaction_sequence = self.intended_interaction.unwrap()
            print "-----------------"
            print self.intended_interaction

        # Enact a primitive interaction from the sequence we are currently
        # enacting.
        intended_interaction = self.enacting_interaction_sequence[self.enacting_interaction_step]
        print "> ", intended_interaction

        # Step 4 of the sequential system, enact the interaction:
        return (intended_interaction, intended_interaction)

    def enacted_interaction(self, interaction_, data):
        self.enacting_interaction_step += 1
        intended_primitive_interaction = data

        self.enacted_sequence.append(interaction_)

        if (
            not interaction_ is intended_primitive_interaction
            or
            self.enacting_interaction_step >= len(self.enacting_interaction_sequence)
            ):
            # Failed or done enacting
            self.enacting_interaction = False

            # Reconstruct enacted interaction from hierarchy of intended
            # interaction
            enacted = self.intended_interaction.reconstruct_from_hierarchy(self.enacted_sequence)

            # Step 5: add new or reinforce existing composite interactions
            learned_or_reinforced = []
            for pre_interaction in self.context:
                composite = interaction.CompositeInteraction(pre_interaction, enacted)
                learned_or_reinforced.append(composite)
                if composite not in self.interaction_memory.get_composite_interactions():
                    self.interaction_memory.add_interaction(composite)
                else:
                    self.interaction_memory.increment_weight(composite)

            # Step 6: update context
            self.update_context(enacted, learned_or_reinforced)
        else: 
            # Not done
            pass

    def setup_interaction_memory(self):
        self.interaction_memory = interactionmemory.InteractionMemory()