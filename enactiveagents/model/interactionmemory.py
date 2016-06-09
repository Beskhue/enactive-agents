"""
Module that holds classes that represent an agent's memory of interactions.
"""

import interaction

class InteractionMemory(object):
    """
    Class to represent the interaction memory of an agent.
    """
    def __init__(self):
        self.primitive_interactions = []
        self.composite_interactions = []
        self.valences = {}
        self.weights = {}

    def add_interaction(self, interaction_, weight=1, valence=0):
        """
        Add an interaction to the interaction memory.

        :param interaction_: The interaction to add.
        :param weight: The weight of the interaction.
        :param valence: The valence of the interaction, only used for primitive
                        interactions.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            self.primitive_interactions.append(interaction_)
            self.valences[interaction_] = valence
        elif isinstance(interaction_, interaction.CompositeInteraction):
            self.composite_interactions.append(interaction_)
        else:
            raise TypeError("Expected interaction_ to be either primitive or composite.")

        self.weights[interaction_] = weight

    def increment_weight(self, interaction):
        """
        Increment the weight of an interaction.

        :param interaction: The interaction to increment the weight of.
        """
        self.weights[interaction] += 1

    def set_weight(self, interaction, weight):
        """
        Set the weight of an interaction to a specific value.

        :param interaction: The interaction to set the weight of.
        :param weight: The value to set the interaction's weight to.
        """
        self.weights[interaction] = weight

    def get_weight(self, interaction):
        """
        Get the weight of an interaction.

        :param interaction: The interaction to get the weight of.
        """
        return self.weights[interaction]

    def set_valence(self, interaction_, valence):
        """
        Set the valence of an interaction to a specific value.

        :param interaction_: The interaction to set the valence of.
        :param valence: The value to set the interaction's valence to.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            self.valences[interaction_] = valence
        else:
            raise TypeError("Expected interaction to be primitive.")

    def get_valence(self, interaction_):
        """
        Get the valence of an interaction. If the interaction is a primative,
        get its valence. If the interaction is composite, sum the valences
        of its primitives.

        :param interaction_: The interaction to get the valence of.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            return self.valences[interaction_]
        elif isinstance(interaction_, interaction.CompositeInteraction):
            primitives = interaction_.unwrap()
            valence = reduce(lambda x, y: x + self.valences[y], primitives, 0)
            return valence
        else:
            raise TypeError("Expected interaction_ to be either primitive or composite.")

    def get_proclivity(self, interaction):
        """
        Get the proclivity of an interaction. Proclivity is defined as the 
        valence multiplied by the weight.

        :param interaction: The interaction to get the proclivity of.
        """
        return self.get_weight(interaction) * self.get_valence(interaction)

    def get_primitive_interactions(self):
        return self.primitive_interactions

    def get_composite_interactions(self):
        return self.composite_interactions

    def get_all_interactions(self):
        return self.primitive_interactions + self.composite_interactions

class HomeostaticInteractionMemory(InteractionMemory):
    """
    A homeostatic interaction's valence is a function of the agent's internal
    energy level. Thus, this interaction memory keeps track of the agent to be
    able to compute the valence.
    """
    def __init__(self, agent):
        super(HomeostaticInteractionMemory, self).__init__()
        self.agent = agent

    def get_valence(self, interaction_):
        """
        Get the valence of an interaction. If the interaction is a primative,
        get its valence. If the interaction is composite, sum the valences
        of its primitives. 

        The valences are functions of the agent's internal energy levels.

        :param interaction_: The interaction to get the valence of.
        """
        if isinstance(interaction_, interaction.PrimitiveInteraction):
            return self.valences[interaction_](self.agent)
        elif isinstance(interaction_, interaction.CompositeInteraction):
            primitives = interaction_.unwrap()
            valence = reduce(lambda x, y: x + self.valences[y](self.agent), primitives, 0)
            return valence
        else:
            raise TypeError("Expected interaction_ to be either primitive or composite.")